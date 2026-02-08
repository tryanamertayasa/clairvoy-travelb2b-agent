"use client";

import { useState } from "react";
import { CopilotSidebar } from "@copilotkit/react-ui";
import { useCoAgent, useCoAgentStateRender } from "@copilotkit/react-core";
import { Navbar } from "@/components/Navbar";
import { HeroSection } from "@/components/HeroSection";
import SupplierCard from "@/components/SupplierCard";
import ValidationSummaryCard from "@/components/ValidationSummaryCard";
import RouteAnalysisCard from "@/components/RouteAnalysisCard";
import CommercialTermsCard from "@/components/CommercialTermsCard";
import GmvProjectionCard from "@/components/GmvProjectionCard";
import DistributionPackageCard from "@/components/DistributionPackageCard";
import { ArtifactViewer } from "@/components/ArtifactViewer";
import type { AgentState } from "@/lib/types";

export default function Home() {
  const [showChat, setShowChat] = useState(false);

  // Connect to agent state
  const { state } = useCoAgent<AgentState>({
    name: "clairvoy_b2b_travel",
  });

  // Render state in chat as generative UI
  useCoAgentStateRender<AgentState>({
    name: "clairvoy_b2b_travel",
    render: ({ state }) => {
      if (!state) return null;

      // Early return during intake
      if (!state.pipeline_stage || state.pipeline_stage === "intake" || !state.stages_completed?.length) {
        if (state.client_name) {
          return (
            <div className="p-3 bg-navy-50 rounded-lg border border-navy-100">
              <div className="flex items-center gap-2">
                <span className="w-2 h-2 bg-maroon-800 rounded-full animate-pulse" />
                <span className="text-navy-900 text-sm font-medium">
                  Processing demand request from {state.client_name}...
                </span>
              </div>
            </div>
          );
        }
        return null;
      }

      // Show simplified progress indicator in chat
      const stageLabels: Record<string, string> = {
        validation: "Assessing feasibility and risks...",
        matching: "Searching supplier inventory...",
        consolidation: "Calculating GMV projections...",
        distribution: "Designing API integration...",
        report: "Generating partnership proposal...",
      };

      const currentLabel = stageLabels[state.pipeline_stage] || `Processing ${state.pipeline_stage}...`;
      const completedCount = state.stages_completed?.length || 0;

      return (
        <div className="p-3 bg-neutral-50 rounded-lg border border-neutral-100">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-2">
              <span className="w-2 h-2 bg-maroon-800 rounded-full animate-pulse" />
              <span className="text-neutral-700 text-sm">{currentLabel}</span>
            </div>
            <span className="text-xs text-neutral-500">
              {completedCount}/6 stages complete
            </span>
          </div>
        </div>
      );
    },
  });

  return (
    <CopilotSidebar
      defaultOpen={showChat}
      clickOutsideToClose={false}
      labels={{
        title: "Clairvoy Assistant",
        initial: `Welcome to Clairvoy, your AI-powered B2B travel consolidation platform.

I connect OTAs, Travel Apps, and TMCs with global travel suppliers through intelligent matching and automated API integration.

**Tell me your requirements:**
- "I need flight and hotel suppliers for Singapore to Bali routes"
- "Find suppliers for Southeast Asia corporate travel programs"
- "Match activity providers for luxury Dubai packages"`,
      }}
    >
      <div className="min-h-screen bg-neutral-50">
        <Navbar />

        {/* Hero Section - shown when no active conversation */}
        {!state?.client_name && (
          <HeroSection onStartAnalysis={() => setShowChat(true)} />
        )}

        <main className={state?.client_name ? "py-8" : "py-0"}>
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            {/* Results Dashboard - shown as data becomes available */}
            {state?.demand_parsed && (
              <div className="space-y-6">
              {/* Demand Overview */}
              {state.client_name && (
                <div className="bg-white rounded-lg border border-neutral-200 p-6 shadow-card">
                  <h3 className="font-display font-semibold text-lg text-neutral-900 mb-4">
                    📋 Client Demand Overview
                  </h3>
                  <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                    <div>
                      <p className="text-xs text-neutral-600 mb-1">Client</p>
                      <p className="font-medium text-neutral-900">{state.client_name}</p>
                    </div>
                    {state.pos_markets && state.pos_markets.length > 0 && (
                      <div>
                        <p className="text-xs text-neutral-600 mb-1">POS Markets</p>
                        <p className="font-medium text-neutral-900">{state.pos_markets.join(", ")}</p>
                      </div>
                    )}
                    {state.routes && (
                      <div>
                        <p className="text-xs text-neutral-600 mb-1">Routes</p>
                        <p className="font-medium text-neutral-900">{state.routes.length}</p>
                      </div>
                    )}
                    {state.product_types && (
                      <div>
                        <p className="text-xs text-neutral-600 mb-1">Products</p>
                        <p className="font-medium text-neutral-900">{state.product_types.join(", ")}</p>
                      </div>
                    )}
                  </div>
                </div>
              )}

              {/* Route Analysis */}
              {state.routes && state.routes.length > 0 && (
                <RouteAnalysisCard routes={state.routes} posMarkets={state.pos_markets} />
              )}

              {/* Commercial Terms */}
              {state.commercial_needs && (
                <CommercialTermsCard terms={state.commercial_needs} />
              )}

              {/* Validation Results */}
              {state.validation_result && (
                <ValidationSummaryCard validation={state.validation_result} />
              )}

              {/* Supplier Inventory Grid */}
              {state.supplier_inventory && state.supplier_inventory.length > 0 && (
                <div>
                  <h3 className="font-display font-semibold text-xl text-neutral-900 mb-4">
                    🌐 Matched Suppliers
                  </h3>
                  <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                    {state.supplier_inventory.map((supplier, index) => (
                      <SupplierCard key={index} supplier={supplier} />
                    ))}
                  </div>
                </div>
              )}

              {/* GMV Projection */}
              {state.gmv_projection && (
                <GmvProjectionCard projection={state.gmv_projection} />
              )}

              {/* Distribution Package */}
              {state.distribution_details && (
                <DistributionPackageCard package={state.distribution_details} />
              )}

              {/* HTML Partnership Proposal */}
              {state.html_report_content && (
                <ArtifactViewer htmlReport={state.html_report_content} />
              )}
              </div>
            )}
          </div>
        </main>
      </div>
    </CopilotSidebar>
  );
}
