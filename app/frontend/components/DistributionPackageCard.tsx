/**
 * DistributionPackageCard Component
 *
 * Displays API distribution package details including
 * endpoints, authentication, rate limits, and white-label options.
 */

import React from 'react';
import { DistributionPackageCardProps } from '@/lib/types';

export default function DistributionPackageCard({ package: pkg }: DistributionPackageCardProps) {
  return (
    <div className="bg-white rounded-lg border border-neutral-200 p-6 shadow-card">
      {/* Header */}
      <h3 className="font-display font-semibold text-lg text-neutral-900 mb-2">
        🔌 API Distribution Package
      </h3>
      <p className="text-sm text-neutral-600 mb-6">Integration specifications and requirements</p>

      {/* API Endpoints */}
      {pkg.api_endpoints && pkg.api_endpoints.length > 0 && (
        <div className="mb-6">
          <h4 className="font-display font-semibold text-sm text-neutral-900 mb-3 flex items-center gap-2">
            <span>🌐</span> API Endpoints
          </h4>
          <div className="space-y-2">
            {pkg.api_endpoints.map((endpoint, index) => (
              <div
                key={index}
                className="p-3 bg-neutral-50 rounded border border-neutral-200 font-mono text-xs text-neutral-800 break-all"
              >
                {endpoint}
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Authentication & Rate Limits - Two Column Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-6">
        {/* Authentication */}
        <div className="p-4 bg-navy-50 rounded-lg border border-navy-100">
          <h4 className="font-display font-semibold text-sm text-navy-900 mb-2 flex items-center gap-2">
            <span>🔐</span> Authentication
          </h4>
          <p className="text-sm text-navy-800">{pkg.authentication_method}</p>
        </div>

        {/* Rate Limits */}
        <div className="p-4 bg-yellow-50 rounded-lg border border-yellow-100">
          <h4 className="font-display font-semibold text-sm text-yellow-900 mb-2 flex items-center gap-2">
            <span>⚡</span> Rate Limits
          </h4>
          <p className="text-sm text-yellow-800">{pkg.rate_limits}</p>
        </div>
      </div>

      {/* White-Label Options */}
      {pkg.white_label_options && pkg.white_label_options.length > 0 && (
        <div className="mb-6">
          <h4 className="font-display font-semibold text-sm text-neutral-900 mb-3 flex items-center gap-2">
            <span>🎨</span> White-Label Options
          </h4>
          <div className="flex flex-wrap gap-2">
            {pkg.white_label_options.map((option, index) => (
              <span
                key={index}
                className="px-3 py-1 bg-maroon-50 text-maroon-700 rounded-full text-xs font-medium border border-maroon-200"
              >
                {option}
              </span>
            ))}
          </div>
        </div>
      )}

      {/* Integration Timeline */}
      {pkg.integration_timeline && (
        <div className="mb-6 p-4 bg-maroon-50 rounded-lg border border-maroon-100">
          <h4 className="font-display font-semibold text-sm text-maroon-900 mb-2 flex items-center gap-2">
            <span>⏱️</span> Integration Timeline
          </h4>
          <p className="text-sm text-maroon-800">{pkg.integration_timeline}</p>
        </div>
      )}

      {/* Technical Requirements */}
      {pkg.technical_requirements && pkg.technical_requirements.length > 0 && (
        <div>
          <h4 className="font-display font-semibold text-sm text-neutral-900 mb-3 flex items-center gap-2">
            <span>⚙️</span> Technical Requirements
          </h4>
          <ul className="space-y-2">
            {pkg.technical_requirements.map((req, index) => (
              <li
                key={index}
                className="text-sm text-neutral-700 flex items-start gap-2"
              >
                <span className="text-navy-800 mt-1">▸</span>
                <span className="flex-1">{req}</span>
              </li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
}
