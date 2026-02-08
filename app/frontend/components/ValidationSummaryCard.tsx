/**
 * ValidationSummaryCard Component
 *
 * Shows feasibility assessment with color-coded grade,
 * risk factors, opportunities, and recommendations.
 */

import React from 'react';
import { ValidationSummaryCardProps } from '@/lib/types';

export default function ValidationSummaryCard({ validation }: ValidationSummaryCardProps) {
  // Feasibility grade styling - Clairvoyy colors
  const gradeStyles = {
    high: {
      bg: 'bg-maroon-50',
      text: 'text-maroon-800',
      border: 'border-maroon-200',
      icon: '✅',
      label: 'High Feasibility',
    },
    medium: {
      bg: 'bg-yellow-50',
      text: 'text-yellow-700',
      border: 'border-yellow-200',
      icon: '⚠️',
      label: 'Medium Feasibility',
    },
    low: {
      bg: 'bg-navy-50',
      text: 'text-navy-900',
      border: 'border-navy-200',
      icon: '❌',
      label: 'Low Feasibility',
    },
  };

  const gradeStyle = gradeStyles[validation.feasibility_grade];

  return (
    <div className="bg-white rounded-lg border border-neutral-200 p-6 shadow-card">
      {/* Header with Grade Badge */}
      <div className="flex items-center gap-4 mb-6">
        <div
          className={`flex items-center gap-2 px-4 py-2 rounded-lg border ${gradeStyle.bg} ${gradeStyle.text} ${gradeStyle.border}`}
        >
          <span className="text-xl">{gradeStyle.icon}</span>
          <span className="font-display font-semibold text-base">{gradeStyle.label}</span>
        </div>
        {validation.estimated_timeline && (
          <span className="text-sm text-neutral-600">
            Timeline: <span className="font-medium text-neutral-900">{validation.estimated_timeline}</span>
          </span>
        )}
      </div>

      {/* Recommendation */}
      <div className="mb-6 p-4 bg-navy-50 border border-navy-100 rounded-lg">
        <h4 className="font-display font-semibold text-sm text-navy-900 mb-2">
          📋 Recommendation
        </h4>
        <p className="text-sm text-navy-800 leading-relaxed">{validation.recommendation}</p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {/* Risk Factors */}
        <div>
          <h4 className="font-display font-semibold text-sm text-neutral-900 mb-3 flex items-center gap-2">
            <span className="text-red-500">⚠️</span>
            Risk Factors
          </h4>
          {validation.risk_factors.length > 0 ? (
            <ul className="space-y-2">
              {validation.risk_factors.map((risk, index) => (
                <li
                  key={index}
                  className="text-sm text-neutral-700 pl-3 border-l-2 border-red-300"
                >
                  {risk}
                </li>
              ))}
            </ul>
          ) : (
            <p className="text-sm text-neutral-500 italic">No significant risks identified</p>
          )}
        </div>

        {/* Opportunities */}
        <div>
          <h4 className="font-display font-semibold text-sm text-neutral-900 mb-3 flex items-center gap-2">
            <span className="text-maroon-800">💡</span>
            Opportunities
          </h4>
          {validation.opportunities.length > 0 ? (
            <ul className="space-y-2">
              {validation.opportunities.map((opportunity, index) => (
                <li
                  key={index}
                  className="text-sm text-neutral-700 pl-3 border-l-2 border-maroon-300"
                >
                  {opportunity}
                </li>
              ))}
            </ul>
          ) : (
            <p className="text-sm text-neutral-500 italic">No opportunities identified</p>
          )}
        </div>
      </div>
    </div>
  );
}
