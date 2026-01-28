//
//  ResultsViewModel.swift
//  Mimikers
//
//  Final score, play again. No Views; bridge to navigation or new game.
//  Layer 3 — ViewModels.
//

import Foundation

/// Results screen state: final score, high score, play again action.
/// Set finalScore (and optionally highScore) from game; play again triggers callback or state reset.
@MainActor
final class ResultsViewModel: ObservableObject {

    // MARK: - Published

    /// Final score from completed game.
    @Published var finalScore: Int = 0
    /// High score (from CardStore or passed in).
    @Published private(set) var highScore: Int = 0
    /// True if this game's score beat the previous high score.
    var isNewHighScore: Bool { finalScore > 0 && finalScore > previousHighScore }

    private var previousHighScore: Int = 0

    // MARK: - Dependencies

    private let cardStore: CardStore

    // MARK: - Init

    init(cardStore: CardStore = CardStore()) {
        self.cardStore = cardStore
    }

    // MARK: - Setup

    /// Set results from game and optionally record score in CardStore. Call when showing results.
    func setResults(finalScore: Int) {
        self.finalScore = finalScore
        previousHighScore = cardStore.highScore
        highScore = cardStore.recordScore(finalScore)
    }

    /// Play again: clear persisted game state so next game starts fresh. Caller handles navigation.
    func playAgain() {
        cardStore.clearSavedState(includingHighScore: false)
    }

    /// Reset displayed score (e.g. when leaving results screen).
    func reset() {
        finalScore = 0
        highScore = cardStore.highScore
        previousHighScore = highScore
    }
}
