/**
 * SupplierCard Component
 *
 * Displays individual supplier inventory (flights/hotels/activities)
 * with availability, pricing model, and coverage information.
 */

import React from 'react';
import { SupplierCardProps } from '@/lib/types';

export default function SupplierCard({ supplier }: SupplierCardProps) {
  // Product type styling - Clairvoyy colors
  const productTypeStyles = {
    flight: 'bg-navy-100 text-navy-900 border-navy-200',
    hotel: 'bg-maroon-100 text-maroon-800 border-maroon-200',
    activity: 'bg-neutral-100 text-neutral-800 border-neutral-300',
  };

  // Availability badge styling
  const getAvailabilityStyle = () => {
    if (supplier.availability.toLowerCase().includes('limited')) {
      return 'badge-warning';
    }
    if (supplier.availability.toLowerCase().includes('wide') ||
        supplier.availability.toLowerCase().includes('extensive')) {
      return 'badge-success';
    }
    return 'bg-neutral-100 text-neutral-800';
  };

  // Product type icon
  const getProductIcon = () => {
    switch (supplier.product_type) {
      case 'flight':
        return '✈️';
      case 'hotel':
        return '🏨';
      case 'activity':
        return '🎯';
      default:
        return '📦';
    }
  };

  return (
    <div className="bg-white rounded-lg border border-neutral-200 p-6 shadow-card hover:shadow-card-hover transition-shadow duration-200">
      {/* Header */}
      <div className="flex items-start justify-between mb-4">
        <div className="flex items-center gap-3">
          <span className="text-3xl">{getProductIcon()}</span>
          <div>
            <h3 className="font-display font-semibold text-lg text-neutral-900">
              {supplier.supplier_name}
            </h3>
            <span
              className={`inline-block mt-1 px-2 py-1 rounded-md text-xs font-medium border ${
                productTypeStyles[supplier.product_type]
              }`}
            >
              {supplier.product_type.charAt(0).toUpperCase() + supplier.product_type.slice(1)}
            </span>
          </div>
        </div>
        <span
          className={`px-3 py-1 rounded-full text-xs font-medium ${getAvailabilityStyle()}`}
        >
          {supplier.availability}
        </span>
      </div>

      {/* Details Grid */}
      <div className="space-y-3">
        <div className="flex justify-between items-center py-2 border-b border-neutral-100">
          <span className="text-sm text-neutral-600">Pricing Model</span>
          <span className="text-sm font-medium text-neutral-900">{supplier.pricing_model}</span>
        </div>

        <div className="flex justify-between items-center py-2 border-b border-neutral-100">
          <span className="text-sm text-neutral-600">Coverage</span>
          <span className="text-sm font-medium text-neutral-900">{supplier.coverage}</span>
        </div>

        {supplier.commission_rate && (
          <div className="flex justify-between items-center py-2 border-b border-neutral-100">
            <span className="text-sm text-neutral-600">Commission</span>
            <span className="text-sm font-medium text-maroon-800">{supplier.commission_rate}</span>
          </div>
        )}

        {supplier.api_integration && (
          <div className="flex justify-between items-center py-2">
            <span className="text-sm text-neutral-600">Integration</span>
            <span className="text-sm font-medium text-neutral-900">{supplier.api_integration}</span>
          </div>
        )}
      </div>
    </div>
  );
}
