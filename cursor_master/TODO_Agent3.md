# TODO List - Agent 3

**Focus**: Layer 3 (ViewModels) - State Management

**Project**: Mimikers iOS — Monikers-style card game for App Store.

This file contains tasks assigned to Agent 3. See master `TODO.md` (or `TODO_TEMPLATE.md`) for full project context.

---

## Mimikers Layer 3 — ViewModels (Complete)

- [x] **HomeViewModel** — deck list, selected deck, start game; load decks on appear; @Published state.
- [x] **GameViewModel** — current card, timer, score, round; bind to GameEngine; start/next/score/end round.
- [x] **ResultsViewModel** — final score, high score, play again; CardStore.recordScore.
- [x] **SettingsViewModel** — timer seconds, number of rounds; bind to SettingsService; save on change.

**Paths**: Mimikers/ViewModels/HomeViewModel.swift, GameViewModel.swift, ResultsViewModel.swift, SettingsViewModel.swift.

---

## MVP Priority Guide — Mimikers iOS

**Ruthless MVP Scope**:
- Load deck; display cards; game flow (rounds, timer, scoring); navigation; persist progress; basic settings.

**Agent 3 key focus**: HomeViewModel (deck list, start game), GameViewModel (current card, timer, score, round; uses GameEngine), ResultsViewModel, SettingsViewModel. Bridge UI ↔ Services; @Published state; Combine. No Views; no raw service calls from Views.

**See `ARCHITECTURE_LAYERS.md` for detailed layer breakdown.**

---

## Layer 3: State Management - ViewModels (Agent 3)

- [x] **Create OnboardingViewModel**
  - **Assignee**: Agent 3
  - **Dependencies**: Layer 2 complete (PhotoLibraryService)
  - **Effort**: Med
  - **Status**: Complete
  - **Notes**:
    - ViewModels/OnboardingViewModel.swift
    - Manage onboarding state
    - Handle permission requests
    - Track onboarding completion
    - Use @Published for state
    - Integrates with PhotoLibraryService for permission handling
    - Multi-step onboarding flow (welcome, permissions, complete)
    - Persists onboarding completion state in UserDefaults
    - Observes authorization status changes reactively
    - Handles permission denied scenarios with settings link

- [x] **Create PhotoLibraryViewModel**
  - **Assignee**: Agent 3
  - **Dependencies**: Layer 2 complete (PhotoLibraryService)
  - **Effort**: Med
  - **Status**: Complete
  - **Notes**:
    - ViewModels/PhotoLibraryViewModel.swift
    - Manage photo library state
    - Load and display photos
    - Handle photo selection
    - Filter and search photos
    - Integrates with PhotoLibraryService for photo enumeration
    - Supports photo selection with max count limits
    - Filtering by media type, date range, and search query
    - Reactive authorization status observation
    - Loading states and error handling
    - Select all/deselect all functionality

- [x] **Create ProcessingViewModel**
  - **Assignee**: Agent 3
  - **Dependencies**: Layer 2 complete (ProcessingPipeline)
  - **Effort**: High
  - **Status**: Complete
  - **Notes**:
    - ViewModels/ProcessingViewModel.swift
    - Manage processing pipeline state
    - Coordinate with ProcessingPipeline service
    - Handle progress updates
    - Manage processing errors
    - Support cancellation
    - Implemented with @MainActor and @Published properties
    - Observes ProcessingPipeline state changes reactively
    - Handles startProcessing(), cancelProcessing(), reset()
    - Error handling with error alerts
    - Processing result management
    - Helper methods for UI (stageDescription, progressPercentage, processingSummary)
    - Configuration management

- [x] **Create ClusterViewModel**
  - **Assignee**: Agent 3
  - **Dependencies**: Layer 2 complete (ClusteringService)
  - **Effort**: Med
  - **Status**: Complete
  - **Notes**:
    - ViewModels/ClusterViewModel.swift
    - Manage cluster viewing state
    - Load clusters from Core Data
    - Handle cluster selection
    - Filter and sort clusters
    - Implemented with @MainActor and @Published properties
    - Loads clusters from Core Data using ClusterEntity
    - Filtering by cluster size (all, large, medium, small)
    - Sorting by date, photo count, and similarity (6 options)
    - Search functionality for clusters
    - Cluster selection management
    - Error handling with error alerts
    - Reactive updates when filters/sort/search change

- [x] **Create AlbumViewModel**
  - **Assignee**: Agent 3
  - **Dependencies**: Layer 2 complete (AlbumManager)
  - **Effort**: Med
  - **Status**: Complete
  - **Notes**:
    - ViewModels/AlbumViewModel.swift
    - Manage album viewing state
    - Load albums from Photos framework
    - Handle album selection
    - Display album contents
    - Implemented with @MainActor and @Published properties
    - Loads albums from Photos framework
    - Loads album metadata from Core Data via AlbumManager
    - Album selection with photo loading
    - Search functionality for albums
    - Helper methods to identify SceneSort-created albums
    - Get cluster ID for albums created from clusters
    - Error handling with error alerts
    - Reactive updates when search query changes

- [x] **Create SettingsViewModel**
  - **Assignee**: Agent 3
  - **Dependencies**: Layer 1 complete (Core Data persistence)
  - **Effort**: Low
  - **Status**: Complete
  - **Notes**:
    - ViewModels/SettingsViewModel.swift
    - Manage app settings
    - Persist user preferences
    - Handle settings changes
    - Implemented with @Published properties for SwiftUI
    - Uses UserDefaults for persistence
    - Includes validation and error handling
    - Settings: batch size, max photos, clustering parameters, processing options

---

**Last Updated**: 2026-01-27
**See Also**:
- `TODO.md` (Master TODO list)
- `CURSOR_BRAIN.md`
- `ARCHITECTURE_LAYERS.md`
- `PROGRESS_LOG.md`

Rules Cursor agents should follow:
- One task = one checkbox line. Everything else is metadata.
- Only set Completed: after the checkbox is [x].
- Prefer Status: over inventing new fields.
- Put detailed implementation notes under Notes: (including file paths and commands).
- Use Subtasks only when it genuinely helps break down work; don't nest deeper than 1 level.
- Check dependencies before starting work on any task.
- Update Status: to "In Progress" when starting a task.
- Update Status: to "Complete" when finishing a task.
