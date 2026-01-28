//
//  CardStore.swift
//  Mimikers
//
//  Save/load game progress and scores. MVP: UserDefaults.
//  Layer 2 — Services.
//

import Foundation

/// Persists last game state and scores. Uses UserDefaults for MVP; can switch to SwiftData/Core Data later.
final class CardStore {

    private let defaults: UserDefaults
    private let stateKey = "com.mimikers.lastGameState"
    private let highScoreKey = "com.mimikers.highScore"
    private let encoder: JSONEncoder
    private let decoder: JSONDecoder

    init(defaults: UserDefaults = .standard) {
        self.defaults = defaults
        self.encoder = JSONEncoder()
        self.decoder = JSONDecoder()
    }

    /// Save current game state (for resume). Does not log raw card content.
    func saveGameState(_ state: GameState) -> Result<Void, AppError> {
        do {
            let data = try encoder.encode(state)
            defaults.set(data, forKey: stateKey)
            return .success(())
        } catch {
            ErrorHandler.log("Save game state failed: \(error.localizedDescription)", level: .error)
            return .failure(.persistenceFailed(reason: error.localizedDescription))
        }
    }

    /// Load last saved game state. Returns nil if none or invalid.
    func loadGameState() -> GameState? {
        guard let data = defaults.data(forKey: stateKey) else { return nil }
        do {
            return try decoder.decode(GameState.self, from: data)
        } catch {
            ErrorHandler.log("Load game state failed: \(error.localizedDescription)", level: .warning)
            return nil
        }
    }

    /// Update high score if the given score is greater. Returns new high score.
    func recordScore(_ score: Int) -> Int {
        let current = defaults.integer(forKey: highScoreKey)
        let newHigh = max(current, score)
        if newHigh > current {
            defaults.set(newHigh, forKey: highScoreKey)
        }
        return newHigh
    }

    /// Last recorded high score.
    var highScore: Int {
        defaults.integer(forKey: highScoreKey)
    }

    /// Clear saved state (e.g. new game). Does not clear high score unless requested.
    func clearSavedState(includingHighScore: Bool = false) {
        defaults.removeObject(forKey: stateKey)
        if includingHighScore {
            defaults.removeObject(forKey: highScoreKey)
        }
    }
}
