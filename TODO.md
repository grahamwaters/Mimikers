# TODO List — Mimikers iOS

This file tracks all tasks, features, bugs, and improvements for the **Mimikers iOS app** (App Store).  
Update after every major action. See `cursor_master/CURSOR_BRAIN.md` for guidelines.

---

## ⚠️ STANDARD PROJECT INITIALIZATION STEP (REQUIRED)

**Before starting implementation, complete this step:**

- [ ] **Research Common Issues & Add Preemptive Fixes**
  - **Assignee**: AI
  - **Dependencies**: None
  - **Effort**: Med
  - **Status**: Todo
  - **Notes**:
    - Search for "Swift SwiftUI iOS common issues 2024"
    - Search for "iOS game App Store rejection issues"
    - Search for "SwiftUI memory leak performance"
    - Search for "iOS permission handling best practices"
    - Add TODO items to preemptively address identified issues
  - **Subtasks**:
    - [ ] Search "Swift SwiftUI common issues 2024"
    - [ ] Search "iOS game App Store rejection"
    - [ ] Search "SwiftUI memory battery"
    - [ ] Search "iOS permission handling best practices"
    - [ ] Add items to "Common Issues & Preemptive Fixes" below
    - [ ] Prioritize by likelihood and impact

---

## MVP Priority Guide

**Ruthless MVP Scope** (Mimikers iOS):

- [ ] Load at least one bundled deck (JSON)
- [ ] Display cards (title hidden; clues visible)
- [ ] Single game flow: deck → round(s) → timer → scoring
- [ ] Simple navigation: home → deck list → game → results
- [ ] Persist last game or scores (SwiftData/Core Data)
- [ ] Basic settings (timer, number of rounds)

**Post-MVP**: iPad, multiplayer, custom decks, IAP, sync.

**MVP order**: 1) Xcode project & Layer 1 → 2) Services → 3) ViewModels → 4) Views → 5) Navigation → 6) Tests & polish.

---

## High-Priority — Project Setup

- [ ] **Initialize Mimikers iOS Xcode project**
  - **Assignee**: AI
  - **Dependencies**: None
  - **Effort**: Med
  - **Status**: Todo
  - **Notes**: Create Mimikers.xcodeproj; targets Mimikers, MimikersTests, MimikersUITests; folders per cursor_master/ARCHITECTURE_LAYERS.md; iOS 17+, Swift 5.9+
  - **Subtasks**:
    - [ ] Create Xcode project and scheme
    - [ ] Add Views, ViewModels, Models, Services, Utilities, Navigation, Resources
    - [ ] Configure signing for simulator

- [ ] **Add sample bundled deck JSON**
  - **Assignee**: AI
  - **Dependencies**: Project exists; Card/Deck model (or placeholder)
  - **Effort**: Low
  - **Status**: Todo
  - **Notes**: Export small deck from config/ (e.g. ppn_deck_copy.json); place in Mimikers/Resources/Decks/; match shape: title, summary, point_value

- [ ] **Configure App icons and launch screen**
  - **Assignee**: AI
  - **Dependencies**: Project exists
  - **Effort**: Low
  - **Status**: Todo
  - **Notes**: Assets.xcassets app icon; LaunchScreen.storyboard or SwiftUI launch

---

## Layer 1 — Foundation (Models, Data, Utilities)

- [x] **Implement Card model**
  - **Assignee**: Agent 1
  - **Dependencies**: Project initialized
  - **Effort**: Low
  - **Status**: DONE
  - **Notes**: Mimikers/Models/Card.swift; properties: title, summary/clues, pointValue; Codable for JSON; match repo JSON shape

- [x] **Implement Deck model**
  - **Assignee**: Agent 1
  - **Dependencies**: Card model
  - **Effort**: Low
  - **Status**: DONE
  - **Notes**: Mimikers/Models/Deck.swift; id, name, cards: [Card]; Codable

- [x] **Implement GameState and GameSettings**
  - **Assignee**: Agent 1
  - **Dependencies**: Card, Deck
  - **Effort**: Med
  - **Status**: DONE
  - **Notes**: GameState (currentRound, score, currentCardIndex, timerRemaining); GameSettings (timerSeconds, numberOfRounds)

- [x] **Implement AppError**
  - **Assignee**: Agent 1
  - **Dependencies**: None
  - **Effort**: Low
  - **Status**: DONE
  - **Notes**: Mimikers/Models/AppError.swift; centralized error types (e.g. deckLoadFailed, invalidData)

- [x] **Implement ErrorHandler and Logger**
  - **Assignee**: Agent 1
  - **Dependencies**: AppError
  - **Effort**: Low
  - **Status**: DONE
  - **Notes**: Mimikers/Utilities/ErrorHandler.swift, Logger.swift; privacy-safe; no sensitive data in logs

- [x] **Set up persistence (SwiftData or Core Data)**
  - **Assignee**: Agent 1
  - **Dependencies**: Project initialized
  - **Effort**: Med
  - **Status**: DONE
  - **Notes**: PersistenceController (UserDefaults for MVP); save/load last game, high scores, GameSettings; SwiftData/Core Data optional later

---

## Layer 2 — Services (Business Logic)

- [x] **Implement DeckLoaderService**
  - **Assignee**: Agent 2
  - **Dependencies**: Card, Deck, AppError
  - **Effort**: Med
  - **Status**: Done
  - **Notes**: Mimikers/Services/DeckLoaderService.swift; load JSON from bundle; parse into Deck; background queue; match config JSON (title, summary, point_value). Supports root array of cards or root object { id, name, cards }. listDeckFilenames for bundle Decks/.

- [x] **Implement GameEngine**
  - **Assignee**: Agent 2
  - **Dependencies**: Card, Deck, GameState, GameSettings
  - **Effort**: High
  - **Status**: Done
  - **Notes**: Mimikers/Services/GameEngine.swift; round state, timer (Combine Timer.publish), next card, scoring, startRound, endRound, advanceToNextRound. statePublisher and timerRemainingPublisher for ViewModels.

- [x] **Implement CardStore (persistence service)**
  - **Assignee**: Agent 2
  - **Dependencies**: Layer 1 persistence, GameState
  - **Effort**: Med
  - **Status**: Done
  - **Notes**: Mimikers/Services/CardStore.swift; save/load GameState and high score; UserDefaults for MVP. No SwiftData/Core Data yet.

- [x] **Implement SettingsService**
  - **Assignee**: Agent 2
  - **Dependencies**: GameSettings
  - **Effort**: Low
  - **Status**: Done
  - **Notes**: Mimikers/Services/SettingsService.swift; read/write timer length and number of rounds via UserDefaults.

---

## Layer 3 — ViewModels (State Management)

- [ ] **Implement HomeViewModel**
  - **Assignee**: Agent 3
  - **Dependencies**: DeckLoaderService
  - **Effort**: Med
  - **Status**: Todo
  - **Notes**: Mimikers/ViewModels/HomeViewModel.swift; deck list, selected deck, start game action; @Published state; load decks on appear

- [ ] **Implement GameViewModel**
  - **Assignee**: Agent 3
  - **Dependencies**: GameEngine, Deck, GameSettings
  - **Effort**: High
  - **Status**: Todo
  - **Notes**: Mimikers/ViewModels/GameViewModel.swift; current card, timer, score, round; start/pause/next; bind to GameEngine

- [ ] **Implement ResultsViewModel**
  - **Assignee**: Agent 3
  - **Dependencies**: GameEngine or final score state
  - **Effort**: Low
  - **Status**: Todo
  - **Notes**: Final score, play again action

- [ ] **Implement SettingsViewModel**
  - **Assignee**: Agent 3
  - **Dependencies**: SettingsService
  - **Effort**: Low
  - **Status**: Todo
  - **Notes**: Timer, rounds; bind to SettingsService

---

## Layer 4 — Views (UI)

- [ ] **Implement HomeView**
  - **Assignee**: Agent 4
  - **Dependencies**: HomeViewModel
  - **Effort**: Med
  - **Status**: Todo
  - **Notes**: Mimikers/Views/HomeView.swift; list of decks; tap to start game; loading/empty state

- [ ] **Implement GameView**
  - **Assignee**: Agent 4
  - **Dependencies**: GameViewModel
  - **Effort**: High
  - **Status**: Todo
  - **Notes**: Mimikers/Views/GameView.swift; card display (clues visible, title hidden until reveal); timer; score; next/skip; tap to reveal title

- [ ] **Implement CardView component**
  - **Assignee**: Agent 4
  - **Dependencies**: Card model
  - **Effort**: Med
  - **Status**: Todo
  - **Notes**: Mimikers/Views/Components/CardView.swift; show clues; optional reveal title; reusable

- [ ] **Implement ResultsView**
  - **Assignee**: Agent 4
  - **Dependencies**: ResultsViewModel
  - **Effort**: Low
  - **Status**: Todo
  - **Notes**: Final score; Play again button

- [ ] **Implement SettingsView**
  - **Assignee**: Agent 4
  - **Dependencies**: SettingsViewModel
  - **Effort**: Low
  - **Status**: Todo
  - **Notes**: Timer picker, rounds picker; save to SettingsService

- [ ] **Implement EmptyStateView and ErrorView components**
  - **Assignee**: Agent 4
  - **Dependencies**: None
  - **Effort**: Low
  - **Status**: Todo
  - **Notes**: Mimikers/Views/Components/; empty deck list; error message display

---

## Layer 5 — Navigation & App Entry

- [ ] **Implement AppNavigation and Route**
  - **Assignee**: Agent 4
  - **Dependencies**: Views exist
  - **Effort**: Med
  - **Status**: Todo
  - **Notes**: Mimikers/Navigation/AppNavigation.swift, Route.swift; NavigationStack; home → game → results; optional settings

- [ ] **Wire up MimikersApp entry point**
  - **Assignee**: Agent 4
  - **Dependencies**: AppNavigation, HomeView
  - **Effort**: Low
  - **Status**: Todo
  - **Notes**: MimikersApp.swift; root view; environment objects if used

---

## Layer 6 — Testing

- [ ] **Unit tests for Card, Deck, GameState**
  - **Assignee**: AI
  - **Dependencies**: Layer 1 models
  - **Effort**: Med
  - **Status**: Todo
  - **Notes**: MimikersTests/Models/; Codable, equality

- [ ] **Unit tests for DeckLoaderService**
  - **Assignee**: AI
  - **Dependencies**: DeckLoaderService
  - **Effort**: Med
  - **Status**: Todo
  - **Notes**: Load bundled JSON; parse; error cases (missing file, invalid JSON)

- [ ] **Unit tests for GameEngine**
  - **Assignee**: AI
  - **Dependencies**: GameEngine
  - **Effort**: High
  - **Status**: Todo
  - **Notes**: Round advance, scoring, next card, timer logic

- [ ] **UI tests for critical flows**
  - **Assignee**: AI
  - **Dependencies**: UI implemented
  - **Effort**: High
  - **Status**: Todo
  - **Notes**: MimikersUITests/; launch → select deck → play round → see results

---

## Layer 7 — Polish & App Store

- [ ] **Accessibility (VoiceOver, Dynamic Type)**
  - **Assignee**: Agent 4
  - **Dependencies**: Views implemented
  - **Effort**: Med
  - **Status**: Todo
  - **Notes**: Labels, hints; test with VoiceOver

- [ ] **Localization (string externalization)**
  - **Assignee**: AI
  - **Dependencies**: Views implemented
  - **Effort**: Med
  - **Status**: Todo
  - **Notes**: Localizable.xcstrings or .strings; at least English

- [ ] **Privacy policy and App Store description**
  - **Assignee**: AI
  - **Dependencies**: None
  - **Effort**: Med
  - **Status**: Todo
  - **Notes**: Required for App Store; explain data (e.g. scores stored on device only)

- [ ] **App Store assets (screenshots, preview)**
  - **Assignee**: AI
  - **Dependencies**: App functional
  - **Effort**: Med
  - **Status**: Todo
  - **Notes**: Icons, screenshots for required sizes; optional preview video

---

## Common Issues & Preemptive Fixes

- [x] **Ensure main-thread compliance**
  - **Assignee**: Agent 2
  - **Dependencies**: Services implemented
  - **Effort**: Low
  - **Status**: Done
  - **Notes**: DeckLoaderService loads and decodes on background queue; completion called on callback queue (default main). GameEngine timer uses RunLoop.main for UI-bound updates.

- [ ] **Memory with large decks**
  - **Assignee**: Agent 2
  - **Dependencies**: DeckLoaderService
  - **Effort**: Med
  - **Status**: Todo
  - **Notes**: If deck is very large, consider streaming or pagination; measure with Instruments

- [ ] **App Store permission descriptions (if any)**
  - **Assignee**: AI
  - **Dependencies**: None
  - **Effort**: Low
  - **Status**: Todo
  - **Notes**: If app later adds permissions, use detailed descriptions to avoid rejection

- [ ] **Privacy manifest / App Store privacy labels**
  - **Assignee**: AI
  - **Dependencies**: App near release
  - **Effort**: Low
  - **Status**: Todo
  - **Notes**: Declare data collection (if any); on-device only = minimal declaration

---

## Documentation

- [ ] **Update README with iOS app section**
  - **Assignee**: AI
  - **Dependencies**: Project exists
  - **Effort**: Low
  - **Status**: Todo
  - **Notes**: How to open Mimikers.xcodeproj; build for simulator; link to cursor_master docs

- [ ] **Document architecture decisions (when stable)**
  - **Assignee**: AI
  - **Dependencies**: MVP complete
  - **Effort**: Med
  - **Status**: Todo
  - **Notes**: Why MVVM, SwiftData vs UserDefaults for MVP, etc.

---

## Post-MVP (Backlog)

- [ ] iPad layout and multi-window
- [ ] Multiple decks / deck categories
- [ ] Custom decks (import JSON)
- [ ] Multiplayer (same device or network)
- [ ] In-app purchase (premium decks)
- [ ] iCloud sync for progress/scores
- [ ] Haptic feedback and sound
- [ ] Dark mode refinement
- [ ] Widget (e.g. “Last score”)

---

**Last Updated**: 2026-01-28  
**Next Review**: After Standard Initialization Step  
**See Also**: `cursor_master/CURSOR_BRAIN.md`, `cursor_master/ARCHITECTURE_LAYERS.md`, `cursor_master/AGENTS.md`

**Rules for agents**: One task = one checkbox; use Status and Notes; Touched Paths when claiming; don’t nest subtasks deeper than one level.
