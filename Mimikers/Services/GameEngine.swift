//
//  GameEngine.swift
//  Mimikers
//
//  Round flow, timer (Combine), next card, scoring. No UI; no ViewModels.
//  Layer 2 — Services.
//

import Foundation
import Combine

/// Game flow: start round, next card, timer tick, scoring, end round.
/// Consumes Deck and GameSettings; produces GameState updates via Combine.
final class GameEngine {

    private var deck: Deck?
    private var settings: GameSettings
    private var state: GameState
    private var timerCancellable: AnyCancellable?
    private let timerSubject = PassthroughSubject<Int, Never>()
    private let stateSubject: CurrentValueSubject<GameState, Never>

    /// Timer remaining seconds (Combine). Emits every second while round is active.
    var timerRemainingPublisher: AnyPublisher<Int, Never> {
        timerSubject.eraseToAnyPublisher()
    }

    /// Current game state. Updated on round start, next card, score, timer tick, end round.
    var statePublisher: AnyPublisher<GameState, Never> {
        stateSubject.eraseToAnyPublisher()
    }

    var currentState: GameState { stateSubject.value }

    init(settings: GameSettings = .default) {
        self.settings = settings
        self.state = GameState()
        self.stateSubject = CurrentValueSubject(GameState())
    }

    /// Configure with a deck and optional settings. Call before startRound.
    func configure(deck: Deck, settings: GameSettings? = nil) {
        if let s = settings { self.settings = s }
        self.deck = deck
        state = GameState(deckId: deck.id)
        stateSubject.send(state)
    }

    /// Start the first round (or next round). Resets timer to settings length; card index can be 0 or preserved.
    func startRound() {
        stopTimer()
        guard let d = deck, !d.cards.isEmpty else { return }
        state.timerRemaining = settings.timerSeconds
        state.currentCardIndex = 0
        stateSubject.send(state)
        startTimer()
    }

    /// Advance to the next card. If no more cards, does not advance; caller can end round.
    func nextCard() {
        guard let d = deck else { return }
        if state.currentCardIndex + 1 < d.cards.count {
            state.currentCardIndex += 1
            stateSubject.send(state)
        }
    }

    /// Add points for the current card (e.g. correct guess). Uses card's pointValue.
    func addScoreForCurrentCard() {
        guard let d = deck, state.currentCardIndex < d.cards.count else { return }
        let points = d.cards[state.currentCardIndex].pointValue
        state.score += points
        stateSubject.send(state)
    }

    /// Set score explicitly (e.g. for skip or custom rules).
    func setScore(_ value: Int) {
        state.score = max(0, value)
        stateSubject.send(state)
    }

    /// End the current round: stop timer, optionally advance to next round.
    func endRound() {
        stopTimer()
    }

    /// Advance to the next round (e.g. after endRound). Resets card index and timer for new round.
    func advanceToNextRound() {
        guard state.currentRound < settings.numberOfRounds else { return }
        state.currentRound += 1
        state.currentCardIndex = 0
        state.timerRemaining = settings.timerSeconds
        stateSubject.send(state)
        startTimer()
    }

    /// Current card if deck and index are valid; nil otherwise.
    func currentCard() -> Card? {
        guard let d = deck, state.currentCardIndex < d.cards.count else { return nil }
        return d.cards[state.currentCardIndex]
    }

    /// Whether there are more cards in the current deck after current index.
    var hasMoreCards: Bool {
        guard let d = deck else { return false }
        return state.currentCardIndex + 1 < d.cards.count
    }

    /// Whether more rounds remain after the current one.
    var hasMoreRounds: Bool {
        state.currentRound < settings.numberOfRounds
    }

    private func startTimer() {
        stopTimer()
        let start = state.timerRemaining
        timerSubject.send(start)
        timerCancellable = Timer.publish(every: 1, on: .main, in: .common)
            .autoconnect()
            .sink { [weak self] _ in
                guard let self = self else { return }
                self.state.timerRemaining = max(0, self.state.timerRemaining - 1)
                self.stateSubject.send(self.state)
                self.timerSubject.send(self.state.timerRemaining)
                if self.state.timerRemaining <= 0 {
                    self.stopTimer()
                }
            }
    }

    private func stopTimer() {
        timerCancellable?.cancel()
        timerCancellable = nil
    }
}
