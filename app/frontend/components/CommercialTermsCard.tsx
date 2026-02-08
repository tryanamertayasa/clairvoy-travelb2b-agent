/**
 * CommercialTermsCard Component
 *
 * Displays payment terms, volume commitments, margin preferences,
 * and credit terms in a structured table layout.
 */

import React from 'react';
import { CommercialTermsCardProps } from '@/lib/types';

export default function CommercialTermsCard({ terms }: CommercialTermsCardProps) {
  // Check if any terms are provided
  const hasTerms =
    terms.payment_terms ||
    terms.volume_commitment ||
    terms.margin_preference ||
    terms.credit_terms;

  if (!hasTerms) {
    return (
      <div className="bg-white rounded-lg border border-neutral-200 p-6 shadow-card">
        <h3 className="font-display font-semibold text-lg text-neutral-900 mb-4">
          💼 Commercial Terms
        </h3>
        <p className="text-sm text-neutral-500 italic">No commercial terms specified</p>
      </div>
    );
  }

  return (
    <div className="bg-white rounded-lg border border-neutral-200 p-6 shadow-card">
      {/* Header */}
      <h3 className="font-display font-semibold text-lg text-neutral-900 mb-6">
        💼 Commercial Terms
      </h3>

      {/* Terms Table */}
      <div className="space-y-4">
        {terms.payment_terms && (
          <div className="pb-4 border-b border-neutral-100">
            <div className="flex items-start justify-between">
              <div className="flex-1">
                <p className="text-sm font-medium text-neutral-700 mb-1">💳 Payment Terms</p>
                <p className="text-sm text-neutral-900">{terms.payment_terms}</p>
              </div>
            </div>
          </div>
        )}

        {terms.volume_commitment && (
          <div className="pb-4 border-b border-neutral-100">
            <div className="flex items-start justify-between">
              <div className="flex-1">
                <p className="text-sm font-medium text-neutral-700 mb-1">📊 Volume Commitment</p>
                <p className="text-sm text-neutral-900">{terms.volume_commitment}</p>
              </div>
            </div>
          </div>
        )}

        {terms.margin_preference && (
          <div className="pb-4 border-b border-neutral-100">
            <div className="flex items-start justify-between">
              <div className="flex-1">
                <p className="text-sm font-medium text-neutral-700 mb-1">💰 Margin Preference</p>
                <p className="text-sm text-neutral-900">{terms.margin_preference}</p>
              </div>
            </div>
          </div>
        )}

        {terms.credit_terms && (
          <div>
            <div className="flex items-start justify-between">
              <div className="flex-1">
                <p className="text-sm font-medium text-neutral-700 mb-1">🏦 Credit Terms</p>
                <p className="text-sm text-neutral-900">{terms.credit_terms}</p>
              </div>
            </div>
          </div>
        )}
      </div>

      {/* Summary Banner */}
      <div className="mt-6 p-4 bg-primary-50 rounded-lg">
        <p className="text-xs text-primary-700">
          <span className="font-medium">Note:</span> Commercial terms are subject to negotiation
          based on final supplier agreements and volume commitments.
        </p>
      </div>
    </div>
  );
}
