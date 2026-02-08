/**
 * GmvProjectionCard Component
 *
 * Displays GMV (Gross Merchandise Value) revenue forecasts
 * with product breakdown and margin estimates.
 */

import React from 'react';
import { GmvProjectionCardProps } from '@/lib/types';

export default function GmvProjectionCard({ projection }: GmvProjectionCardProps) {
  // Format currency
  const formatCurrency = (amount: number): string => {
    return new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency: 'USD',
      minimumFractionDigits: 0,
      maximumFractionDigits: 0,
    }).format(amount);
  };

  // Calculate percentages for product breakdown
  const productBreakdown = Object.entries(projection.breakdown_by_product).map(
    ([product, value]) => ({
      product,
      value,
      percentage: (value / projection.total_gmv) * 100,
    })
  );

  // Product colors - Clairvoyy palette
  const productColors: Record<string, string> = {
    flights: 'bg-navy-800',
    hotels: 'bg-maroon-800',
    activities: 'bg-neutral-500',
    default: 'bg-neutral-500',
  };

  return (
    <div className="bg-white rounded-lg border border-neutral-200 p-6 shadow-card">
      {/* Header */}
      <h3 className="font-display font-semibold text-lg text-neutral-900 mb-2">
        📈 GMV Projection
      </h3>
      <p className="text-sm text-neutral-600 mb-6">Estimated revenue potential</p>

      {/* Total GMV - Big Callout */}
      <div className="mb-6 p-6 bg-gradient-to-br from-navy-50 to-navy-100 rounded-lg border border-navy-200">
        <p className="text-sm font-medium text-navy-700 mb-1">Total Annual GMV</p>
        <p className="font-display font-bold text-4xl text-navy-900">
          {formatCurrency(projection.total_gmv)}
        </p>
        {projection.annual_forecast && (
          <p className="text-sm text-navy-700 mt-2">{projection.annual_forecast}</p>
        )}
      </div>

      {/* Product Breakdown */}
      <div className="mb-6">
        <h4 className="font-display font-semibold text-sm text-neutral-900 mb-4">
          Revenue by Product
        </h4>
        <div className="space-y-3">
          {productBreakdown.map(({ product, value, percentage }) => (
            <div key={product}>
              <div className="flex items-center justify-between mb-1">
                <span className="text-sm font-medium text-neutral-700 capitalize">{product}</span>
                <span className="text-sm font-semibold text-neutral-900">
                  {formatCurrency(value)}
                </span>
              </div>
              <div className="w-full bg-neutral-100 rounded-full h-2">
                <div
                  className={`h-2 rounded-full ${
                    productColors[product.toLowerCase()] || productColors.default
                  }`}
                  style={{ width: `${percentage}%` }}
                />
              </div>
              <div className="text-right mt-1">
                <span className="text-xs text-neutral-600">{percentage.toFixed(1)}%</span>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Margin Estimate */}
      <div className="p-4 bg-maroon-50 border border-maroon-100 rounded-lg">
        <p className="text-sm font-medium text-maroon-900 mb-1">💰 Margin Estimate</p>
        <p className="text-sm text-maroon-800">{projection.margin_estimate}</p>
      </div>
    </div>
  );
}
