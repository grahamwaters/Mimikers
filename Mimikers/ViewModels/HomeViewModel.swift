//
//  HomeViewModel.swift
//  Mimikers
//
//  Deck list, selected deck, start game. Bridge UI ↔ DeckLoaderService.
//  Layer 3 — ViewModels.
//

import Foundation
import Combine

/// Home screen state: deck list, selection, load deck for game start.
/// Uses DeckLoaderService; exposes @Published for SwiftUI. No Views.
@MainActor
final class HomeViewModel: ObservableObject {

    // MARK: - Published

    /// Deck filenames available in bundle (e.g. ["sample.json"]).
    @Published private(set) var deckFilenames: [String] = []
    /// User-selected filename; nil until selected.
    @Published var selectedDeckFilename: String?
    /// True while loading deck list or a single deck.
    @Published private(set) var isLoading = false
    /// Non-nil when deck list or load fails; clear on retry.
    @Published var errorMessage: String?
    /// Loaded deck ready to start game; set after successful loadDeckForGame(), cleared when navigating away.
    @Published private(set) var loadedDeck: Deck?

    // MARK: - Dependencies

    private let deckLoader: DeckLoaderService

    // MARK: - Init

    init(deckLoader: DeckLoaderService = DeckLoaderService()) {
        self.deckLoader = deckLoader
    }

    // MARK: - Actions

    /// Load deck list from bundle. Call on appear.
    func loadDecks() {
        errorMessage = nil
        isLoading = true
        deckFilenames = deckLoader.listDeckFilenames(subdirectory: "Decks")
        isLoading = false
        if deckFilenames.isEmpty {
            errorMessage = "No decks found in bundle."
        }
    }

    /// Load deck by filename and set loadedDeck for navigation to game. Clears previous error.
    func loadDeckForGame(filename: String) {
        guard deckFilenames.contains(filename) else {
            errorMessage = "Deck not found: \(filename)"
            return
        }
        errorMessage = nil
        isLoading = true
        loadedDeck = nil
        deckLoader.loadDeck(filename: filename, subdirectory: "Decks", callbackQueue: .main) { [weak self] result in
            Task { @MainActor in
                self?.isLoading = false
                switch result {
                case .success(let deck):
                    self?.loadedDeck = deck
                case .failure(let error):
                    self?.errorMessage = error.localizedDescription
                }
            }
        }
    }

    /// Start game with currently selected filename (if any). Loads deck and sets loadedDeck.
    func startGame() {
        guard let name = selectedDeckFilename else {
            errorMessage = "Select a deck first."
            return
        }
        loadDeckForGame(filename: name)
    }

    /// Clear loaded deck (e.g. when leaving game or after navigation).
    func clearLoadedDeck() {
        loadedDeck = nil
    }

    /// Clear error message (e.g. user dismisses alert).
    func clearError() {
        errorMessage = nil
    }
}
