/**
 * RouteAnalysisCard Component
 *
 * Displays origin→destination routes with demand indicators
 * and POS market information.
 */

import React from 'react';
import { RouteAnalysisCardProps } from '@/lib/types';

export default function RouteAnalysisCard({ routes, posMarkets }: RouteAnalysisCardProps) {
  // Demand level styling
  const getDemandStyle = (level?: 'high' | 'medium' | 'low') => {
    switch (level) {
      case 'high':
        return 'bg-accent-100 text-accent-800';
      case 'medium':
        return 'bg-yellow-100 text-yellow-800';
      case 'low':
        return 'bg-neutral-100 text-neutral-800';
      default:
        return 'bg-neutral-100 text-neutral-700';
    }
  };

  return (
    <div className="bg-white rounded-lg border border-neutral-200 p-6 shadow-card">
      {/* Header */}
      <div className="flex items-center justify-between mb-6">
        <div>
          <h3 className="font-display font-semibold text-lg text-neutral-900">
            🗺️ Route Analysis
          </h3>
          <p className="text-sm text-neutral-600 mt-1">
            {routes.length} route{routes.length !== 1 ? 's' : ''} analyzed
          </p>
        </div>
        {posMarkets && posMarkets.length > 0 && (
          <div className="text-right">
            <p className="text-xs text-neutral-600 mb-1">POS Markets</p>
            <div className="flex gap-1 flex-wrap justify-end">
              {posMarkets.map((market, index) => (
                <span
                  key={index}
                  className="px-2 py-1 bg-primary-50 text-primary-700 rounded text-xs font-medium"
                >
                  {market}
                </span>
              ))}
            </div>
          </div>
        )}
      </div>

      {/* Routes List */}
      <div className="space-y-4">
        {routes.map((route, index) => (
          <div
            key={index}
            className="p-4 bg-neutral-50 rounded-lg border border-neutral-100 hover:border-primary-200 transition-colors"
          >
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-3 flex-1">
                {/* Origin */}
                <div className="text-center">
                  <p className="text-xs text-neutral-600 mb-1">From</p>
                  <p className="font-display font-semibold text-sm text-neutral-900">
                    {route.origin}
                  </p>
                </div>

                {/* Arrow */}
                <div className="text-primary-400">
                  <svg
                    className="w-8 h-8"
                    fill="none"
                    stroke="currentColor"
                    viewBox="0 0 24 24"
                  >
                    <path
                      strokeLinecap="round"
                      strokeLinejoin="round"
                      strokeWidth={2}
                      d="M13 7l5 5m0 0l-5 5m5-5H6"
                    />
                  </svg>
                </div>

                {/* Destination */}
                <div className="text-center">
                  <p className="text-xs text-neutral-600 mb-1">To</p>
                  <p className="font-display font-semibold text-sm text-neutral-900">
                    {route.destination}
                  </p>
                </div>
              </div>

              {/* Demand Badge */}
              {route.demand_level && (
                <span
                  className={`px-3 py-1 rounded-full text-xs font-medium whitespace-nowrap ml-4 ${getDemandStyle(
                    route.demand_level
                  )}`}
                >
                  {route.demand_level.charAt(0).toUpperCase() + route.demand_level.slice(1)} Demand
                </span>
              )}
            </div>
          </div>
        ))}
      </div>

      {routes.length === 0 && (
        <div className="text-center py-8">
          <p className="text-sm text-neutral-500 italic">No routes specified</p>
        </div>
      )}
    </div>
  );
}
