"use client";

import { useState, useMemo, useCallback } from "react";
import type { AgentState, TimelineStepConfig, CollapsedSteps } from "@/lib/types";
import { CollapsibleStep } from "./CollapsibleStep";
import { StepOutputContent } from "./StepOutputContent";

/**
 * Timeline step configurations for B2B travel consolidation pipeline.
 */
const TIMELINE_STEPS: TimelineStepConfig[] = [
  {
    id: "intake",
    label: "Demand Intake",
    stageKey: "intake",
    tool: { icon: "📋", name: "parse_demand" },
  },
  {
    id: "validation",
    label: "Validation & Feasibility",
    stageKey: "validation",
    tool: { icon: "✅", name: "assess_feasibility" },
  },
  {
    id: "matching",
    label: "Supplier Matching",
    stageKey: "matching",
    tool: { icon: "🔍", name: "gds_search" },
  },
  {
    id: "consolidation",
    label: "Inventory Consolidation",
    stageKey: "consolidation",
    tool: { icon: "📊", name: "gmv_analysis" },
  },
  {
    id: "distribution",
    label: "Distribution Design",
    stageKey: "distribution",
    tool: { icon: "🔌", name: "api_design" },
  },
  {
    id: "report",
    label: "Partnership Proposal",
    stageKey: "report",
    tool: { icon: "📄", name: "html_report" },
  },
];

interface PipelineTimelineProps {
  state: AgentState;
  currentStage?: string;
  completedStages: string[];
}

/**
 * PipelineTimeline - Main dashboard component showing the pipeline journey.
 *
 * Features:
 * - Header card with business info and score
 * - Collapsible steps for each pipeline stage
 * - Real-time progress tracking
 * - Tool badges and output summaries
 */
export function PipelineTimeline({
  state,
  currentStage,
  completedStages,
}: PipelineTimelineProps) {
  // Track collapsed state for each step (default: all expanded)
  const [collapsed, setCollapsed] = useState<CollapsedSteps>({});

  // Toggle collapse state for a step
  const toggleStep = useCallback((stepId: string) => {
    setCollapsed((prev) => ({
      ...prev,
      [stepId]: !prev[stepId],
    }));
  }, []);

  // Determine status for each step
  const getStepStatus = useCallback(
    (step: TimelineStepConfig): "pending" | "in_progress" | "complete" => {
      if (completedStages.includes(step.stageKey)) {
        return "complete";
      }
      if (currentStage === step.stageKey || currentStage === step.id) {
        return "in_progress";
      }
      return "pending";
    },
    [completedStages, currentStage]
  );

  // Calculate progress
  const completedCount = completedStages.length;
  const progressPercent = Math.round((completedCount / TIMELINE_STEPS.length) * 100);

  // Check if intake step should show (when client_name is set)
  const showIntake = Boolean(state.client_name);

  return (
    <div className="bg-white rounded-xl shadow-card border border-neutral-200 overflow-hidden">
      {/* Header Card - Client Info */}
      <div className="p-6 bg-gradient-to-r from-primary-50 to-white border-b border-neutral-100">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-4">
            <div className="h-14 w-14 bg-gradient-to-br from-primary-500 to-primary-600 rounded-xl flex items-center justify-center shadow-lg">
              <span className="text-2xl">✈️</span>
            </div>
            <div>
              <h2 className="font-display text-xl font-semibold text-neutral-900">
                {state.client_name || "B2B Travel Demand"}
              </h2>
              <p className="text-neutral-600 text-sm">
                {state.product_types?.join(", ") || "Multi-product consolidation"}
              </p>
            </div>
          </div>

          {/* Progress indicator */}
          <div className="text-right">
            <div className="text-sm text-neutral-500 mb-1">
              {completedCount}/{TIMELINE_STEPS.length} stages complete
            </div>
            <div className="w-32 h-2 bg-neutral-200 rounded-full overflow-hidden">
              <div
                className="h-full bg-gradient-to-r from-primary-500 to-accent-500 transition-all duration-500"
                style={{ width: `${progressPercent}%` }}
              />
            </div>
          </div>
        </div>
      </div>

      {/* Timeline Steps */}
      <div className="p-4 space-y-3">
        {TIMELINE_STEPS.map((step, index) => {
          const status = getStepStatus(step);

          // For intake, show when target_location is set
          // For other steps, show based on current progress
          const shouldShow =
            step.id === "intake"
              ? showIntake
              : completedStages.includes(step.stageKey) ||
                currentStage === step.stageKey ||
                currentStage === step.id ||
                // Show next pending step
                (status === "pending" &&
                  index > 0 &&
                  (completedStages.includes(TIMELINE_STEPS[index - 1].stageKey) ||
                   currentStage === TIMELINE_STEPS[index - 1].stageKey));

          if (!shouldShow) return null;

          // Intake is "complete" if client_name is set
          const actualStatus =
            step.id === "intake" && showIntake
              ? "complete"
              : status;

          // Always expand current step, use collapsed state for completed
          const isExpanded =
            actualStatus === "in_progress" || !collapsed[step.id];

          return (
            <CollapsibleStep
              key={step.id}
              step={step}
              stepNumber={index + 1}
              status={actualStatus}
              isExpanded={isExpanded}
              onToggle={() => toggleStep(step.id)}
            >
              <StepOutputContent stepId={step.id} state={state} />
            </CollapsibleStep>
          );
        })}
      </div>

      {/* All Complete indicator */}
      {completedCount === TIMELINE_STEPS.length && (
        <div className="p-4 bg-accent-50 border-t border-accent-100">
          <div className="flex items-center justify-center gap-2 text-accent-700">
            <span className="text-xl">✅</span>
            <span className="font-medium">Partnership Proposal Ready</span>
          </div>
        </div>
      )}
    </div>
  );
}
