import React from 'react';

interface HeroSectionProps {
  onStartAnalysis: () => void;
}

export const HeroSection = ({ onStartAnalysis }: HeroSectionProps) => {
  const features = [
    {
      icon: '🎯',
      title: 'AI-Powered Supplier Matching',
      description:
        'Intelligent algorithms match your requirements with the best suppliers in real-time.',
    },
    {
      icon: '📊',
      title: 'Commercial Feasibility Assessment',
      description:
        'Comprehensive evaluation of market viability, pricing strategies, and risk factors.',
    },
    {
      icon: '📋',
      title: 'Partnership Proposal Generation',
      description:
        'Automated creation of professional, data-driven partnership proposals.',
    },
  ];

  return (
    <div className="relative bg-gradient-to-br from-navy-900 via-navy-800 to-navy-900 text-white overflow-hidden">
      {/* Decorative background elements */}
      <div className="absolute inset-0 opacity-10">
        <div className="absolute top-20 right-20 w-64 h-64 bg-maroon-500 rounded-full blur-3xl"></div>
        <div className="absolute bottom-20 left-20 w-96 h-96 bg-navy-600 rounded-full blur-3xl"></div>
      </div>

      {/* Main content */}
      <div className="relative max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-16 md:py-24">
        <div className="text-center space-y-6 mb-16">
          {/* Tagline */}
          <div className="flex items-center justify-center space-x-2 text-maroon-300">
            <span className="text-xl">✈️</span>
            <span className="font-medium tracking-wide uppercase text-sm">
              Expert Insights, Smarter Decisions
            </span>
          </div>

          {/* Main heading */}
          <h1 className="font-display text-4xl md:text-5xl lg:text-6xl font-bold leading-tight">
            Transforming Travel
            <br />
            and Aviation Trade
          </h1>

          {/* Description */}
          <p className="max-w-2xl mx-auto text-lg md:text-xl text-neutral-200 leading-relaxed">
            Comprehensive platform for B2B travel consolidation. Our AI-powered
            solution provides intelligent supplier matching, feasibility
            assessment, and automated partnership proposals.
          </p>

          {/* CTA Button */}
          <div className="pt-4">
            <button
              onClick={onStartAnalysis}
              className="btn-primary text-lg px-8 py-4"
            >
              Start Analysis
            </button>
          </div>
        </div>

        {/* Feature Cards */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
          {features.map((feature, index) => (
            <div
              key={index}
              className="bg-white/10 backdrop-blur-sm rounded-xl p-6 border border-white/20 hover:bg-white/15 transition-all"
            >
              <div className="text-5xl mb-4">{feature.icon}</div>
              <h3 className="font-display font-semibold text-xl mb-3">
                {feature.title}
              </h3>
              <p className="text-neutral-300 leading-relaxed">
                {feature.description}
              </p>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};
