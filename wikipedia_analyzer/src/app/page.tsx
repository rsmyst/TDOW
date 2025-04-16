"use client";

import { useState, useEffect, useRef } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { useRouter } from "next/navigation";

// PathStatistics component
const PathStatistics = () => {
  const [statistics, setStatistics] = useState<any>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    const fetchStatistics = async () => {
      try {
        const response = await fetch("http://localhost:8000/path-statistics");
        if (!response.ok) {
          throw new Error("Failed to fetch statistics");
        }
        const data = await response.json();
        setStatistics(data);
      } catch (err) {
        setError((err as Error).message || "An error occurred");
      } finally {
        setIsLoading(false);
      }
    };

    fetchStatistics();
  }, []);

  if (isLoading) {
    return (
      <div className="bg-gray-800 p-6 rounded-lg shadow-2xl h-full flex items-center justify-center">
        <svg className="animate-spin h-8 w-8 text-blue-400" viewBox="0 0 24 24">
          <circle
            className="opacity-25"
            cx="12"
            cy="12"
            r="10"
            stroke="currentColor"
            strokeWidth="4"
          ></circle>
          <path
            className="opacity-75"
            fill="currentColor"
            d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
          ></path>
        </svg>
      </div>
    );
  }

  if (error) {
    return (
      <div className="bg-gray-800 p-6 rounded-lg shadow-2xl h-full">
        <h2 className="text-xl font-semibold mb-4 text-red-400">Error</h2>
        <p className="text-red-300">{error}</p>
      </div>
    );
  }

  if (!statistics) return null;

  // Format path length distribution for display
  const pathDistribution = statistics.path_stats.path_length_distribution;
  const totalPaths = Object.values(pathDistribution).reduce(
    (acc: number, val: any) => acc + val,
    0
  );

  // Get the longest path found (either max_path_length or approximate_diameter)
  const longestPath = statistics.path_stats.approximate_diameter;

  return (
    <div className="bg-gray-800 p-6 rounded-lg shadow-2xl h-full">
      <h2 className="text-xl font-semibold mb-4 bg-gradient-to-r from-blue-400 to-purple-500 text-transparent bg-clip-text">
        Wikipedia Graph Stats
      </h2>

      {/* Longest Path Highlight */}
      <div className="mb-5 p-3 bg-gradient-to-r from-blue-500/20 to-purple-600/20 rounded-lg border border-blue-500/30">
        <div className="text-center">
          <h3 className="text-lg font-medium text-white">Longest Path Found</h3>
          <div className="text-3xl font-bold mt-1 bg-gradient-to-r from-blue-400 to-purple-500 text-transparent bg-clip-text">
            {longestPath} links
          </div>
          <p className="text-xs text-gray-400 mt-1">
            Maximum distance between any two articles in the network
          </p>
        </div>
      </div>

      <div className="space-y-4">
        <div>
          <h3 className="text-lg font-medium text-gray-300 mb-1">
            Graph Overview
          </h3>
          <div className="grid grid-cols-2 gap-2 text-sm">
            <div className="bg-gray-700 p-2 rounded">
              <span className="text-gray-400">Nodes:</span>{" "}
              {statistics.graph_info.num_nodes.toLocaleString()}
            </div>
            <div className="bg-gray-700 p-2 rounded">
              <span className="text-gray-400">Edges:</span>{" "}
              {statistics.graph_info.num_edges.toLocaleString()}
            </div>
            <div className="bg-gray-700 p-2 rounded">
              <span className="text-gray-400">Avg Degree:</span>{" "}
              {statistics.graph_info.avg_degree.toFixed(1)}
            </div>
            <div className="bg-gray-700 p-2 rounded">
              <span className="text-gray-400">Components:</span>{" "}
              {statistics.component_stats.num_components}
            </div>
          </div>
        </div>

        <div>
          <h3 className="text-lg font-medium text-gray-300 mb-1">
            Path Information
          </h3>
          <div className="grid grid-cols-2 gap-2 text-sm">
            <div className="bg-gray-700 p-2 rounded">
              <span className="text-gray-400">Avg Length:</span>{" "}
              {statistics.path_stats.avg_path_length.toFixed(2)}
            </div>
            <div className="bg-gray-700 p-2 rounded">
              <span className="text-gray-400">Max Length:</span>{" "}
              {statistics.path_stats.max_path_length}
            </div>
          </div>
        </div>

        <div>
          <h3 className="text-lg font-medium text-gray-300 mb-1">
            Path Distribution
          </h3>
          <div className="space-y-1">
            {Object.entries(pathDistribution)
              .sort((a, b) => parseInt(a[0]) - parseInt(b[0]))
              .map(([length, count]: [string, any]) => (
                <div key={length} className="flex items-center">
                  <div className="w-8 text-gray-400">{length}:</div>
                  <div className="flex-1 h-5 bg-gray-700 rounded overflow-hidden">
                    <div
                      className="h-full bg-gradient-to-r from-blue-500 to-purple-600"
                      style={{ width: `${(count / totalPaths) * 100}%` }}
                    ></div>
                  </div>
                  <div className="ml-2 text-xs text-gray-400">
                    {((count / totalPaths) * 100).toFixed(1)}%
                  </div>
                </div>
              ))}
          </div>
          <p className="text-xs text-gray-500 mt-2">
            Most Wikipedia articles are connected by{" "}
            {statistics.path_stats.avg_path_length.toFixed(0)} links
          </p>
        </div>
      </div>
    </div>
  );
};

export default function Home() {
  const [source, setSource] = useState("");
  const [destination, setDestination] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [result, setResult] = useState<null | {
    path: string[];
    distance: number;
  }>(null);
  const [error, setError] = useState("");

  // Autocomplete states
  const [sourceSuggestions, setSourceSuggestions] = useState<string[]>([]);
  const [destSuggestions, setDestSuggestions] = useState<string[]>([]);
  const [activeField, setActiveField] = useState<
    "source" | "destination" | null
  >(null);

  // Refs for handling outside clicks
  const sourceInputRef = useRef<HTMLInputElement>(null);
  const destInputRef = useRef<HTMLInputElement>(null);
  const sourceSuggestionsRef = useRef<HTMLDivElement>(null);
  const destSuggestionsRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    // Handle clicks outside the autocomplete
    const handleClickOutside = (event: MouseEvent) => {
      if (
        sourceInputRef.current &&
        sourceSuggestionsRef.current &&
        !sourceInputRef.current.contains(event.target as Node) &&
        !sourceSuggestionsRef.current.contains(event.target as Node)
      ) {
        setActiveField((prev) => (prev === "source" ? null : prev));
      }

      if (
        destInputRef.current &&
        destSuggestionsRef.current &&
        !destInputRef.current.contains(event.target as Node) &&
        !destSuggestionsRef.current.contains(event.target as Node)
      ) {
        setActiveField((prev) => (prev === "destination" ? null : prev));
      }
    };

    document.addEventListener("mousedown", handleClickOutside);
    return () => document.removeEventListener("mousedown", handleClickOutside);
  }, []);

  useEffect(() => {
    const fetchSuggestions = async (
      query: string,
      field: "source" | "destination"
    ) => {
      if (query.length < 2) {
        field === "source" ? setSourceSuggestions([]) : setDestSuggestions([]);
        return;
      }

      try {
        const response = await fetch(
          `http://localhost:8000/suggest?q=${encodeURIComponent(query)}`
        );
        if (response.ok) {
          const data = await response.json();
          field === "source"
            ? setSourceSuggestions(data)
            : setDestSuggestions(data);
        }
      } catch (err) {
        console.error("Error fetching suggestions:", err);
      }
    };

    // Debounce input to prevent too many requests
    const handler = setTimeout(() => {
      if (activeField === "source") {
        fetchSuggestions(source, "source");
      } else if (activeField === "destination") {
        fetchSuggestions(destination, "destination");
      }
    }, 300);

    return () => clearTimeout(handler);
  }, [source, destination, activeField]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!source || !destination) return;

    setIsLoading(true);
    setError("");
    setResult(null);

    try {
      const response = await fetch("http://localhost:8000/find-path", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ source, destination }),
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.detail || "Failed to find path");
      }

      setResult(data);
    } catch (err) {
      setError((err as Error).message || "An error occurred");
    } finally {
      setIsLoading(false);
    }
  };

  const handleSuggestionClick = (
    suggestion: string,
    field: "source" | "destination"
  ) => {
    if (field === "source") {
      setSource(suggestion);
      setSourceSuggestions([]);
    } else {
      setDestination(suggestion);
      setDestSuggestions([]);
    }
    setActiveField(null);
  };

  return (
    <div className="min-h-screen bg-gray-900 text-white flex flex-col items-center justify-center p-4">
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.8 }}
        className="w-full max-w-6xl"
      >
        <h1 className="text-4xl font-bold text-center mb-2 bg-gradient-to-r from-blue-400 to-purple-500 text-transparent bg-clip-text">
          Three Degrees of Wikipedia
        </h1>
        <p className="text-gray-400 text-center mb-8">
          Find the shortest path between any two Wikipedia articles
        </p>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-8">
          <motion.form
            onSubmit={handleSubmit}
            className="bg-gray-800 p-6 rounded-lg shadow-2xl"
            initial={{ scale: 0.95 }}
            animate={{ scale: 1 }}
            transition={{ duration: 0.5 }}
          >
            <div className="mb-4 relative">
              <label className="block text-gray-300 mb-2">Source Article</label>
              <input
                ref={sourceInputRef}
                type="text"
                value={source}
                onChange={(e) => setSource(e.target.value)}
                onFocus={() => setActiveField("source")}
                className="w-full p-3 bg-gray-700 rounded-md border border-gray-600 focus:border-blue-500 focus:ring-2 focus:ring-blue-500 focus:outline-none transition-all"
                placeholder="e.g. Albert Einstein"
              />

              <AnimatePresence>
                {activeField === "source" && sourceSuggestions.length > 0 && (
                  <motion.div
                    ref={sourceSuggestionsRef}
                    initial={{ opacity: 0, y: -10 }}
                    animate={{ opacity: 1, y: 0 }}
                    exit={{ opacity: 0, y: -10 }}
                    transition={{ duration: 0.2 }}
                    className="absolute z-10 mt-1 w-full bg-gray-700 border border-gray-600 rounded-md shadow-lg overflow-hidden"
                  >
                    {sourceSuggestions.map((suggestion, index) => (
                      <motion.div
                        key={index}
                        initial={{ opacity: 0, x: -5 }}
                        animate={{ opacity: 1, x: 0 }}
                        transition={{ delay: index * 0.03 }}
                        className="p-3 hover:bg-gray-600 cursor-pointer transition-colors"
                        onClick={() =>
                          handleSuggestionClick(suggestion, "source")
                        }
                      >
                        {suggestion}
                      </motion.div>
                    ))}
                  </motion.div>
                )}
              </AnimatePresence>
            </div>

            <div className="mb-6 relative">
              <label className="block text-gray-300 mb-2">
                Destination Article
              </label>
              <input
                ref={destInputRef}
                type="text"
                value={destination}
                onChange={(e) => setDestination(e.target.value)}
                onFocus={() => setActiveField("destination")}
                className="w-full p-3 bg-gray-700 rounded-md border border-gray-600 focus:border-blue-500 focus:ring-2 focus:ring-blue-500 focus:outline-none transition-all"
                placeholder="e.g. Quantum Physics"
              />

              <AnimatePresence>
                {activeField === "destination" &&
                  destSuggestions.length > 0 && (
                    <motion.div
                      ref={destSuggestionsRef}
                      initial={{ opacity: 0, y: -10 }}
                      animate={{ opacity: 1, y: 0 }}
                      exit={{ opacity: 0, y: -10 }}
                      transition={{ duration: 0.2 }}
                      className="absolute z-10 mt-1 w-full bg-gray-700 border border-gray-600 rounded-md shadow-lg overflow-hidden"
                    >
                      {destSuggestions.map((suggestion, index) => (
                        <motion.div
                          key={index}
                          initial={{ opacity: 0, x: -5 }}
                          animate={{ opacity: 1, x: 0 }}
                          transition={{ delay: index * 0.03 }}
                          className="p-3 hover:bg-gray-600 cursor-pointer transition-colors"
                          onClick={() =>
                            handleSuggestionClick(suggestion, "destination")
                          }
                        >
                          {suggestion}
                        </motion.div>
                      ))}
                    </motion.div>
                  )}
              </AnimatePresence>
            </div>

            <motion.button
              type="submit"
              className="w-full py-3 bg-gradient-to-r from-blue-500 to-purple-600 rounded-md font-medium hover:from-blue-600 hover:to-purple-700 transition-all"
              whileHover={{ scale: 1.02 }}
              whileTap={{ scale: 0.98 }}
              disabled={isLoading || !source || !destination}
            >
              {isLoading ? (
                <span className="flex items-center justify-center">
                  <svg
                    className="animate-spin h-5 w-5 mr-2"
                    viewBox="0 0 24 24"
                  >
                    <circle
                      className="opacity-25"
                      cx="12"
                      cy="12"
                      r="10"
                      stroke="currentColor"
                      strokeWidth="4"
                    ></circle>
                    <path
                      className="opacity-75"
                      fill="currentColor"
                      d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
                    ></path>
                  </svg>
                  Finding Path...
                </span>
              ) : (
                "Find Path"
              )}
            </motion.button>
          </motion.form>

          {/* Path Statistics Component */}
          <motion.div
            initial={{ opacity: 0, scale: 0.95 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ duration: 0.5, delay: 0.1 }}
          >
            <PathStatistics />
          </motion.div>
        </div>

        {error && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            className="p-4 mb-6 bg-red-500/20 border border-red-500/50 text-red-200 rounded-md"
          >
            {error}
          </motion.div>
        )}

        {result && (
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5, delay: 0.2 }}
            className="bg-gray-800 p-6 rounded-lg shadow-xl"
          >
            <h2 className="text-xl font-semibold mb-4">
              Path Found! Distance: {result.distance}
            </h2>
            <div className="space-y-3">
              {result.path.map((article, index) => (
                <motion.div
                  key={index}
                  initial={{ opacity: 0, x: -10 }}
                  animate={{ opacity: 1, x: 0 }}
                  transition={{ delay: index * 0.1 }}
                  className="flex items-center"
                >
                  <div className="w-8 h-8 rounded-full bg-blue-500 flex items-center justify-center font-bold">
                    {index + 1}
                  </div>
                  <div className="ml-3 flex-1 p-3 bg-gray-700 rounded-md">
                    {article}
                  </div>
                </motion.div>
              ))}
            </div>
          </motion.div>
        )}
      </motion.div>
    </div>
  );
}
