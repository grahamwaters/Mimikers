//
//  SettingsViewModel.swift
//  Mimikers
//
//  Timer and rounds; bind to SettingsService. No Views.
//  Layer 3 — ViewModels.
//

import Foundation
import Combine

/// Settings screen state: timer seconds, number of rounds. Bridges UI ↔ SettingsService.
@MainActor
final class SettingsViewModel: ObservableObject {

    // MARK: - Published

    @Published var timerSeconds: Int {
        didSet {
            if timerSeconds != oldValue {
                applyTimerToService()
            }
        }
    }

    @Published var numberOfRounds: Int {
        didSet {
            if numberOfRounds != oldValue {
                applyRoundsToService()
            }
        }
    }

    /// Non-nil when save fails.
    @Published var errorMessage: String?

    // MARK: - Dependencies

    private let settingsService: SettingsService

    // MARK: - Init

    init(settingsService: SettingsService = SettingsService()) {
        self.settingsService = settingsService
        let settings = settingsService.load()
        self.timerSeconds = settings.timerSeconds
        self.numberOfRounds = settings.numberOfRounds
    }

    // MARK: - Load

    /// Reload from SettingsService (e.g. on appear).
    func load() {
        let settings = settingsService.load()
        timerSeconds = settings.timerSeconds
        numberOfRounds = settings.numberOfRounds
        errorMessage = nil
    }

    // MARK: - Apply

    private func applyTimerToService() {
        let clamped = max(1, timerSeconds)
        if clamped != timerSeconds { timerSeconds = clamped }
        switch settingsService.setTimerSeconds(clamped) {
        case .success:
            errorMessage = nil
        case .failure(let error):
            errorMessage = error.localizedDescription
        }
    }

    private func applyRoundsToService() {
        let clamped = max(1, numberOfRounds)
        if clamped != numberOfRounds { numberOfRounds = clamped }
        switch settingsService.setNumberOfRounds(clamped) {
        case .success:
            errorMessage = nil
        case .failure(let error):
            errorMessage = error.localizedDescription
        }
    }

    /// Save current values to SettingsService (e.g. explicit Save button).
    func save() {
        let settings = GameSettings(timerSeconds: timerSeconds, numberOfRounds: numberOfRounds)
        switch settingsService.save(settings) {
        case .success:
            errorMessage = nil
        case .failure(let error):
            errorMessage = error.localizedDescription
        }
    }

    func clearError() {
        errorMessage = nil
    }
}
