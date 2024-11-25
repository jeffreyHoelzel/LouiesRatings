import React from 'react';
import { Link } from 'react-router-dom';

const ProfessorList = ({ professors, handleProfessorClick }) => {
  if (!professors || professors.length === 0) {
    return (
      <div className="professors-list mt-4">
        <p className="text-gray-500">No professors found for this class.</p>
      </div>
    );
  }

  return (
    <div className="professors-list mt-4">
      <ul className="space-y-2">
        {professors.map((professor, index) => (
          <li 
            key={index}
            className="p-3 bg-white rounded-lg shadow-sm hover:shadow-md transition-shadow duration-200"
            onClick={() => handleProfessorClick(professor)}  // Use the click handler
          >
            <Link 
               to={`/professor/${encodeURIComponent(professor.toLowerCase().replace(/\s+/g, '-'))}`}
              className="flex items-center justify-between text-blue-600 hover:text-blue-800"
            >
              <span>{professor}</span>
              <svg 
                className="w-5 h-5" 
                fill="none" 
                stroke="currentColor" 
                viewBox="0 0 24 24"
              >
                <path 
                  strokeLinecap="round" 
                  strokeLinejoin="round" 
                  strokeWidth={2} 
                  d="M9 5l7 7-7 7" 
                />
              </svg>
            </Link>
          </li>
        ))}
      </ul>
    </div>
  );
};

export default ProfessorList;