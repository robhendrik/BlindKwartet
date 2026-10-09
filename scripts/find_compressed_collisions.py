"""Print the first compressed-key collisions in sampled depth-3 states."""

from __future__ import annotations

import argparse
from collections import defaultdict
import random
from dataclasses import replace

from blind_kwartet.category_projection import project_category_bitmap
from blind_kwartet.compressed_search_key import CompressedSearchKey, compressed_search_key
from blind_kwartet.deals import CARDS, CARDS_PER_CATEGORY, INITIAL_DEALS, N_CATEGORIES
from blind_kwartet.global_search_diagnostics import sample_global_tree
from blind_kwartet.moves import AnswerMove, QuestionMove
from blind_kwartet.players import _GlobalSearch
from blind_kwartet.search import SymmetryTransform, canonical_key, transform_state
from blind_kwartet.search_state import SearchState
from blind_kwartet.single_category_solver import SingleCategorySolver


def _state(key: tuple[int, tuple[int, ...], int]) -> SearchState:
    return SearchState(
        possible_initial_deals=key[0],
        current_owner_override=key[1],
        actor=key[2],
    )


def _exact_state_text(state: SearchState) -> str:
    return (
        "SearchState("
        f"D=0x{state.D:x}, T={state.T!r}, actor={state.actor})"
    )


def _world_ids(bitmap: int) -> tuple[int, ...]:
    result = []
    while bitmap:
        low = bitmap & -bitmap
        result.append(low.bit_length() - 1)
        bitmap ^= low
    return tuple(result)


def _projected_world_sets(state: SearchState) -> tuple[tuple[int, ...], ...]:
    return tuple(
        _world_ids(project_category_bitmap(state, category, state.actor))
        for category in range(N_CATEGORIES)
    )


def _count_table(deal_id: int) -> tuple[tuple[int, ...], ...]:
    owners = INITIAL_DEALS[deal_id].owner_by_card
    return tuple(
        tuple(
            owners[category * CARDS_PER_CATEGORY:
                   (category + 1) * CARDS_PER_CATEGORY].count(player)
            for player in range(3)
        )
        for category in range(N_CATEGORIES)
    )


def _witnesses(first: SearchState, second: SearchState) -> tuple[tuple[int, tuple[int, ...]], ...]:
    only_first = first.D & ~second.D
    only_second = second.D & ~first.D
    witnesses = []
    for mask, state_side in ((only_first, 0), (only_second, 1)):
        if mask:
            low = mask & -mask
            deal_id = low.bit_length() - 1
            witnesses.append((state_side, (deal_id, INITIAL_DEALS[deal_id].owner_by_card)))
    return tuple(witnesses)


def _minimal_explanation(first: SearchState, second: SearchState) -> str:
    witnesses = _witnesses(first, second)
    if len(witnesses) < 2:
        return (
            "The exact D sets differ, but no witness exists in both symmetric "
            "directions; compare the printed D masks."
        )
    first_id, first_world = witnesses[0][1]
    second_id, second_world = witnesses[1][1]
    return (
        "The compressed key preserves the same count-table set and per-card "
        "owner projections, but not the joint correlation selecting which "
        "category count patterns occur together. In particular, deal "
        f"{first_id} with owners {first_world} survives only in the first "
        f"state, while deal {second_id} with owners {second_world} survives "
        "only in the second."
    )


def _state_key(state: SearchState) -> tuple[int, tuple[int, ...], int]:
    return (state.D, state.T, state.actor)


class _ParentTracker:
    """Diagnostic-only first-parent graph for sampled exact states."""

    def __init__(self) -> None:
        self.state_ids: dict[tuple[int, tuple[int, ...], int], int] = {}
        self.states: dict[int, SearchState] = {}
        self.parents: dict[int, tuple[int, QuestionMove, AnswerMove]] = {}

    def retain(
        self,
        state: SearchState,
        parent: SearchState | None = None,
        question: QuestionMove | None = None,
        answer: AnswerMove | None = None,
    ) -> int:
        key = _state_key(state)
        state_id = self.state_ids.get(key)
        if state_id is not None:
            return state_id
        state_id = len(self.state_ids) + 1
        self.state_ids[key] = state_id
        self.states[state_id] = state
        if parent is not None and question is not None and answer is not None:
            parent_id = self.retain(parent)
            self.parents[state_id] = (parent_id, question, answer)
        return state_id

    def history(self, state: SearchState) -> tuple[tuple[QuestionMove, AnswerMove, SearchState], ...]:
        state_id = self.state_ids[_state_key(state)]
        reversed_history = []
        while state_id in self.parents:
            parent_id, question, answer = self.parents[state_id]
            reversed_history.append((question, answer, self.states[state_id]))
            state_id = parent_id
        return tuple(reversed(reversed_history))


def _compact_t(state: SearchState) -> str:
    return "".join("-" if owner < 0 else str(owner) for owner in state.T)


def _print_history(label: str, tracker: _ParentTracker, state: SearchState) -> None:
    print(f"{label}:")
    history = tracker.history(state)
    if not history:
        print("  (initial state)")
    current = SearchState.initial()
    for index, (question, answer, successor) in enumerate(history, start=1):
        print(
            f"  {index}. P{current.actor + 1} asks P{question.target + 1} "
            f"{CARDS[question.card]} -> {'YES' if answer.yes else 'NO'}"
        )
        print(
            f"     actor=P{successor.actor + 1}, |D|={successor.D.bit_count()}, "
            f"compact T={_compact_t(successor)}"
        )
        current = successor
    print(f"  final category projections: {_projected_world_sets(state)}")


def _print_first_divergence(
    tracker: _ParentTracker, first: SearchState, second: SearchState
) -> None:
    first_history = tracker.history(first)
    second_history = tracker.history(second)
    first_actor = SearchState.initial().actor
    for index, (left, right) in enumerate(zip(first_history, second_history), start=1):
        if left[:2] != right[:2]:
            left_parent = first_actor if index == 1 else first_history[index - 2][2].actor
            right_parent = first_actor if index == 1 else second_history[index - 2][2].actor
            print(
                f"first path divergence: transition {index}: "
                f"A=P{left_parent + 1} asks P{left[0].target + 1} "
                f"{CARDS[left[0].card]} -> {'YES' if left[1].yes else 'NO'}; "
                f"B=P{right_parent + 1} asks P{right[0].target + 1} "
                f"{CARDS[right[0].card]} -> {'YES' if right[1].yes else 'NO'}"
            )
            print(
                "The differing question/answer filters create different joint "
                "cross-category correlations in D; the compressed key retains "
                "the same local projections and count-table combinations but "
                "drops that world-to-world correlation."
            )
            return
    if len(first_history) != len(second_history):
        print(f"first path divergence: transition {min(len(first_history), len(second_history)) + 1}")
    else:
        print("first path divergence: none in the retained parent histories")


def _fast_reachable_sample(samples: int, depth: int, seed: int):
    """Sample stable question/answer branches without repeated stabilization.

    The authoritative transition masks and legality checks are still used.
    Branches that would require forced-quartet/actor stabilization are skipped;
    this keeps the collision reporter practical while retaining stable states.
    """
    rng = random.Random(seed)
    from blind_kwartet.global_search_diagnostics import GlobalDuplicateRecorder

    recorder = GlobalDuplicateRecorder(canonical_sample=0, compressed_key_sample=0)
    tracker = _ParentTracker()
    for _ in range(samples):
        state = SearchState.initial()
        remaining = depth
        while True:
            tracker.retain(state)
            recorder.record(state, remaining)
            if remaining == 0:
                break
            questions = []
            for category in range(N_CATEGORIES):
                for offset in range(CARDS_PER_CATEGORY):
                    card = category * CARDS_PER_CATEGORY + offset
                    for target in ((state.actor + 1) % 3, (state.actor + 2) % 3):
                        move = QuestionMove(target, category, card)
                        questions.append(move)
            if not questions:
                break
            rng.shuffle(questions)
            context = None
            move = None
            for candidate_move in questions:
                try:
                    context = state.apply_question(candidate_move)
                    move = candidate_move
                    break
                except ValueError:
                    continue
            if context is None or move is None:
                break
            answer_yes = bool(rng.randrange(2))
            if answer_yes and context.yes_mask:
                overrides = list(context.state.T)
                overrides[move.card] = state.actor
                candidate = replace(
                    context.state,
                    possible_initial_deals=context.yes_mask,
                    current_owner_override=tuple(overrides),
                    actor=state.actor,
                ).normalize_overrides()
                answer = AnswerMove(True)
            elif context.no_mask:
                candidate = replace(
                    context.state,
                    possible_initial_deals=context.no_mask,
                    actor=move.target,
                ).normalize_overrides()
                answer = AnswerMove(False)
            else:
                continue
            if candidate.forced_quartets():
                continue
            tracker.retain(candidate, state, move, answer)
            state = candidate
            remaining -= 1
    return recorder, samples, tracker


def _fast_frontier_sample(limit: int, depth: int):
    """Enumerate a bounded legal question/answer frontier cheaply."""
    from blind_kwartet.global_search_diagnostics import GlobalDuplicateRecorder

    recorder = GlobalDuplicateRecorder(canonical_sample=0, compressed_key_sample=0)
    tracker = _ParentTracker()
    def visit(state: SearchState, remaining: int) -> None:
        if len(recorder.by_depth[0]) >= limit:
            return
        recorder.record(state, remaining)
        tracker.retain(state)
        if remaining == 0:
            return
        candidates = []
        for category in range(N_CATEGORIES):
            for offset in range(CARDS_PER_CATEGORY):
                card = category * CARDS_PER_CATEGORY + offset
                for target in ((state.actor + 1) % 3, (state.actor + 2) % 3):
                    candidates.append(QuestionMove(target, category, card))
        for move in candidates:
            try:
                context = state.apply_question(move)
            except ValueError:
                continue
            for yes in (True, False):
                if yes and context.yes_mask:
                    overrides = list(context.state.T)
                    overrides[move.card] = state.actor
                    successor = replace(
                        context.state,
                        possible_initial_deals=context.yes_mask,
                        current_owner_override=tuple(overrides),
                        actor=state.actor,
                    ).normalize_overrides()
                    answer = AnswerMove(True)
                elif not yes and context.no_mask:
                    successor = replace(
                        context.state,
                        possible_initial_deals=context.no_mask,
                        actor=move.target,
                    ).normalize_overrides()
                    answer = AnswerMove(False)
                else:
                    continue
                if successor.forced_quartets():
                    continue
                tracker.retain(successor, state, move, answer)
                visit(successor, remaining - 1)
                if len(recorder.by_depth[0]) >= limit:
                    return
    visit(SearchState.initial(), depth)
    return recorder, limit, tracker


def _print_key(key: CompressedSearchKey) -> None:
    print(f"compressed key: {key!r}")
    print(f"surviving count-table combinations ({len(key.count_tables)}):")
    for table in key.count_tables:
        print(f"  {table}")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--samples", type=int, default=100)
    parser.add_argument("--depth", type=int, default=3)
    parser.add_argument("--remaining-depth", type=int, default=0)
    parser.add_argument("--limit", type=int, default=5)
    parser.add_argument("--seed", type=int, default=123)
    parser.add_argument("--fast-reachable", action="store_true")
    parser.add_argument("--fast-frontier", action="store_true")
    parser.add_argument(
        "--augment-valid-category-symmetry", action="store_true",
        help="add a category-renamed copy of each sampled state for diagnostic collision coverage",
    )
    parser.add_argument(
        "--non-equivalent-only", action="store_true",
        help="exclude collisions also identified by the exhaustive valid canonicalizer",
    )
    args = parser.parse_args()

    if args.fast_frontier:
        recorder, paths, tracker = _fast_frontier_sample(args.samples, args.depth)
    elif args.fast_reachable:
        recorder, paths, tracker = _fast_reachable_sample(args.samples, args.depth, args.seed)
    else:
        recorder, paths = sample_global_tree(args.samples, args.depth, seed=args.seed)
        tracker = _ParentTracker()
    states = [
        _state(key)
        for key in sorted(recorder.by_depth[args.remaining_depth])
    ]
    if args.augment_valid_category_symmetry:
        category_swap = SymmetryTransform(
            (0, 1, 2), (1, 0, 2),
            (tuple(range(4)),) * 3,
        )
        states.extend(transform_state(state, category_swap) for state in states)
    groups: dict[CompressedSearchKey, list[SearchState]] = defaultdict(list)
    for state in states:
        groups[compressed_search_key(state)].append(state)
    collisions = []
    for key, members in groups.items():
        if len(members) <= 1:
            continue
        exact_canonical_groups: dict[tuple[int, int], list[SearchState]] = {}
        if args.non_equivalent_only:
            exact_canonical_groups = defaultdict(list)
            for member in members:
                exact_canonical_groups[canonical_key(member)].append(member)
            if len(exact_canonical_groups) == 1:
                continue
        collisions.append((key, members, exact_canonical_groups))
    collisions.sort(key=lambda item: (min(state.D for state in item[1]), repr(item[0])))

    print(
        f"sampled paths={paths}, depth={args.depth}, "
        f"remaining_depth={args.remaining_depth}, "
        f"exact_states={len(states)}, collision_classes={len(collisions)}"
    )
    if not collisions:
        print("No compressed-key collisions found in this sample.")
        return

    solver = SingleCategorySolver()
    search = _GlobalSearch(solver)
    for index, (key, members, exact_canonical_groups) in enumerate(collisions[:args.limit], start=1):
        first, second = members[:2]
        print(f"\n=== collision {index} ===")
        print(f"exact class size: {len(members)}")
        print(f"exhaustive valid-symmetry classes: {len(exact_canonical_groups)}")
        print(f"first exact state: {_exact_state_text(first)}")
        print(f"second exact state: {_exact_state_text(second)}")
        print(f"first actor={first.actor}, |D|={first.D.bit_count()}, compact T={''.join('-' if x < 0 else str(x) for x in first.T)}")
        print(f"second actor={second.actor}, |D|={second.D.bit_count()}, compact T={''.join('-' if x < 0 else str(x) for x in second.T)}")
        _print_key(key)
        print(f"first projected category world sets: {_projected_world_sets(first)}")
        print(f"second projected category world sets: {_projected_world_sets(second)}")
        print(f"first legal questions: {first.legal_questions()}")
        print(f"second legal questions: {second.legal_questions()}")
        print(f"first leaf value vector: {search._leaf_value(first)}")
        print(f"second leaf value vector: {search._leaf_value(second)}")
        _print_history("State A", tracker, first)
        _print_history("State B", tracker, second)
        _print_first_divergence(tracker, first, second)
        print(f"cross-category explanation: {_minimal_explanation(first, second)}")
        print("witness full worlds:")
        for side, witness in _witnesses(first, second):
            deal_id, owners = witness
            print(f"  state={'first' if side == 0 else 'second'} deal_id={deal_id} owners={owners} count_table={_count_table(deal_id)}")


if __name__ == "__main__":
    main()
