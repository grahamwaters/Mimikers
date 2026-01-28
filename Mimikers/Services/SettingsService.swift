//
//  SettingsService.swift
//  Mimikers
//
//  Read/write timer length and number of rounds. UserDefaults.
//  Layer 2 — Services.
//

import Foundation

/// Persists and reads game settings (timer, rounds). Uses UserDefaults.
final class SettingsService {

    private let defaults: UserDefaults
    private let timerKey = "com.mimikers.timerSeconds"
    private let roundsKey = "com.mimikers.numberOfRounds"

    init(defaults: UserDefaults = .standard) {
        self.defaults = defaults
    }

    /// Load current settings. Returns default if never set.
    func load() -> GameSettings {
        let timer = defaults.object(forKey: timerKey) as? Int ?? GameSettings.default.timerSeconds
        let rounds = defaults.object(forKey: roundsKey) as? Int ?? GameSettings.default.numberOfRounds
        return GameSettings(
            timerSeconds: max(1, timer),
            numberOfRounds: max(1, rounds)
        )
    }

    /// Save settings. Fails with AppError if write fails (e.g. invalid values).
    func save(_ settings: GameSettings) -> Result<Void, AppError> {
        let timer = max(1, settings.timerSeconds)
        let rounds = max(1, settings.numberOfRounds)
        defaults.set(timer, forKey: timerKey)
        defaults.set(rounds, forKey: roundsKey)
        if defaults.synchronize() == false {
            ErrorHandler.log("Settings sync failed", level: .warning)
        }
        return .success(())
    }

    /// Update only timer seconds.
    func setTimerSeconds(_ seconds: Int) -> Result<Void, AppError> {
        var s = load()
        s.timerSeconds = max(1, seconds)
        return save(s)
    }

    /// Update only number of rounds.
    func setNumberOfRounds(_ rounds: Int) -> Result<Void, AppError> {
        var s = load()
        s.numberOfRounds = max(1, rounds)
        return save(s)
    }
}
