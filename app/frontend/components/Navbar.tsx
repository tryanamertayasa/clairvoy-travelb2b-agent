import React from 'react';

export const Navbar = () => {
  return (
    <nav className="sticky top-0 z-50 bg-navy-900 text-white shadow-lg">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16">
          {/* Logo */}
          <div className="flex items-center space-x-2">
            <span className="text-2xl">✈️</span>
            <span className="font-display font-bold text-xl">Clairvoy</span>
          </div>

          {/* Right section - Contact Info */}
          <div className="hidden md:flex items-center space-x-8 text-sm">
            <div className="flex items-center space-x-2">
              <svg
                className="w-4 h-4"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"
                />
              </svg>
              <span className="font-medium">Working Hour:</span>
              <span>08:00am to 05:00pm</span>
            </div>
            <div className="flex items-center space-x-2">
              <svg
                className="w-4 h-4"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z"
                />
              </svg>
              <span className="font-medium">Email:</span>
              <a
                href="mailto:support@clairvoyhub.com"
                className="hover:text-maroon-300 transition-colors"
              >
                support@clairvoyhub.com
              </a>
            </div>
          </div>
        </div>
      </div>
    </nav>
  );
};
