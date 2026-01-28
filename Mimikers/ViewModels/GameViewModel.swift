//
//  GameViewModel.swift
//  Mimikers
//
//  Current card, timer, score, round. Binds to GameEngine; no Views.
//  Layer 3 — ViewModels.
//

import Foundation
import Combine

/// Game play state: current card, timer, score, round. Bridges UI ↔ GameEngine.
/// Configure with deck and settings, then start round; expose @Published for SwiftUI.
@MainActor
final class GameViewModel: ObservableObject {

    // MARK: - Published (from GameEngine)

    @Published private(set) var currentCard: Card?
    @Published private(set) var timerRemaining: Int = 0
    @Published private(set) var score: Int = 0
    @Published private(set) var currentRound: Int = 1
    @Published private(set) var currentCardIndex: Int = 0
    @Published private(set) var totalCards: Int = 0
    /// True when round timer has reached zero.
    @Published private(set) var isTimerExpired = false
    /// Non-nil on engine or flow error.
    @Published var errorMessage: String?

    /// Whether more cards remain in current round.
    var hasMoreCards: Bool { gameEngine.hasMoreCards }
    /// Whether more rounds remain after current.
    var hasMoreRounds: Bool { gameEngine.hasMoreRounds }

    // MARK: - Dependencies

    private let gameEngine: GameEngine
    private var cancellables = Set<AnyCancellable>()

    // MARK: - Init

    init(gameEngine: GameEngine = GameEngine()) {
        self.gameEngine = gameEngine
        subscribeToEngine()
    }

    // MARK: - Configuration

    /// Configure engine with deck and settings; call before startRound().
    func configure(deck: Deck, settings: GameSettings) {
        gameEngine.configure(deck: deck, settings: settings)
        totalCards = deck.cards.count
        applyState(gameEngine.currentState)
    }

    private func subscribeToEngine() {
        gameEngine.statePublisher
            .receive(on: DispatchQueue.main)
            .sink { [weak self] state in
                self?.applyState(state)
            }
            .store(in: &cancellables)

        gameEngine.timerRemainingPublisher
            .receive(on: DispatchQueue.main)
            .sink { [weak self] remaining in
                self?.timerRemaining = remaining
                self?.isTimerExpired = (remaining <= 0)
            }
            .store(in: &cancellables)
    }

    private func applyState(_ state: GameState) {
        score = state.score
        currentRound = state.currentRound
        currentCardIndex = state.currentCardIndex
        timerRemaining = state.timerRemaining
        isTimerExpired = (state.timerRemaining <= 0)
        currentCard = gameEngine.currentCard()
    }

    // MARK: - Actions

    /// Start first round (or next round). Resets timer and card index for the round.
    func startRound() {
        errorMessage = nil
        gameEngine.startRound()
        applyState(gameEngine.currentState)
    }

    /// Advance to next card in current round.
    func nextCard() {
        gameEngine.nextCard()
        applyState(gameEngine.currentState)
    }

    /// Add points for current card (correct guess).
    func addScoreForCurrentCard() {
        gameEngine.addScoreForCurrentCard()
        applyState(gameEngine.currentState)
    }

    /// End current round (stops timer).
    func endRound() {
        gameEngine.endRound()
        applyState(gameEngine.currentState)
    }

    /// Advance to next round; call after endRound when moving to next round.
    func advanceToNextRound() {
        gameEngine.advanceToNextRound()
        applyState(gameEngine.currentState)
    }

    /// Current game state (e.g. for passing to ResultsViewModel or persistence).
    var state: GameState {
        gameEngine.currentState
    }

    /// Clear error message.
    func clearError() {
        errorMessage = nil
    }
}
