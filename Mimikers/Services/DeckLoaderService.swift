//
//  DeckLoaderService.swift
//  Mimikers
//
//  Load JSON decks from bundle; parse into Deck. Background queue; no main-thread blocking.
//  Layer 2 — Services.
//

import Foundation

/// Loads deck JSON from the app bundle and parses into Deck/Card.
/// All file I/O and decoding runs on a background queue.
final class DeckLoaderService: Sendable {

    private let bundle: Bundle
    private let queue: DispatchQueue
    private let decoder: JSONDecoder

    init(
        bundle: Bundle = .main,
        queue: DispatchQueue = DispatchQueue(label: "com.mimikers.deckloader", qos: .userInitiated)
    ) {
        self.bundle = bundle
        self.queue = queue
        self.decoder = JSONDecoder()
    }

    /// Load a deck by filename (e.g. "sample_deck.json") from the bundle.
    /// Returns on the provided callback queue (default main); decoding runs on background.
    func loadDeck(
        filename: String,
        subdirectory: String? = "Decks",
        callbackQueue: DispatchQueue = .main,
        completion: @escaping (Result<Deck, AppError>) -> Void
    ) {
        queue.async { [weak self] in
            guard let self = self else { return }
            let result = self.loadDeckSync(filename: filename, subdirectory: subdirectory)
            callbackQueue.async {
                completion(result)
            }
        }
    }

    /// Synchronous load (for tests or when already on background). Prefer loadDeck for UI.
    func loadDeckSync(filename: String, subdirectory: String? = "Decks") -> Result<Deck, AppError> {
        guard let url = subdirectory != nil
            ? bundle.url(forResource: filename.replacingOccurrences(of: ".json", with: ""), withExtension: "json", subdirectory: subdirectory)
            : bundle.url(forResource: filename.replacingOccurrences(of: ".json", with: ""), withExtension: "json")
        else {
            ErrorHandler.log("Deck file not found: \(filename)", level: .warning)
            return .failure(.deckLoadFailed(reason: "File not found: \(filename)"))
        }
        return loadDeckSync(url: url, fallbackName: (url.deletingPathExtension().lastPathComponent))
    }

    /// Load from a file URL (e.g. bundle resource URL).
    func loadDeckSync(url: URL, fallbackName: String? = nil) -> Result<Deck, AppError> {
        let data: Data
        do {
            data = try Data(contentsOf: url)
        } catch {
            ErrorHandler.log("Deck read failed: \(error.localizedDescription)", level: .error)
            return .failure(.deckLoadFailed(reason: error.localizedDescription))
        }
        return decodeDeck(from: data, fallbackId: url.lastPathComponent, fallbackName: fallbackName ?? url.deletingPathExtension().lastPathComponent)
    }

    /// Decode deck from data. Supports root array of cards (repo shape) or root object { id, name, cards }.
    private func decodeDeck(from data: Data, fallbackId: String, fallbackName: String) -> Result<Deck, AppError> {
        if let deck = try? decoder.decode(Deck.self, from: data) {
            return .success(deck)
        }
        if let cards = try? decoder.decode([Card].self, from: data) {
            let deck = Deck(id: fallbackId, name: fallbackName, cards: cards)
            return .success(deck)
        }
        ErrorHandler.log("Deck decode failed: invalid JSON shape", level: .error)
        return .failure(.invalidData(reason: "Deck JSON must be an array of cards or { id, name, cards }"))
    }

    /// List deck filenames in the bundle subdirectory (e.g. "Decks").
    func listDeckFilenames(subdirectory: String = "Decks") -> [String] {
        guard let resourcePath = bundle.resourcePath else { return [] }
        let decksPath = (resourcePath as NSString).appendingPathComponent(subdirectory)
        guard let contents = try? FileManager.default.contentsOfDirectory(atPath: decksPath) else { return [] }
        return contents.filter { $0.hasSuffix(".json") }.sorted()
    }
}
