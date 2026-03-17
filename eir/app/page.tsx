'use client';

import { useState, useEffect, useMemo } from 'react';

export default function Home() {
  const [displayTitle, setDisplayTitle] = useState('');
  const [displaySubtitle, setDisplaySubtitle] = useState('');
  const [showTitleCursor, setShowTitleCursor] = useState(true);
  const [showSubtitleCursor, setShowSubtitleCursor] = useState(false);
  const [animationComplete, setAnimationComplete] = useState(false);
  const [isExpanding, setIsExpanding] = useState(false);
  const [blobTransforming, setBlobTransforming] = useState(false);
  const [avatarVisible, setAvatarVisible] = useState(false);
  const [showChat, setShowChat] = useState(false);
  const [showChatContent, setShowChatContent] = useState(false);
  const [messages, setMessages] = useState<Array<{role: 'user' | 'assistant', content: string}>>([]);
  const [inputMessage, setInputMessage] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [showButtonOptions, setShowButtonOptions] = useState(false);
  const [remediesVisible, setRemediesVisible] = useState(false);
  const [remedySearchTerm, setRemedySearchTerm] = useState('');
  const [satisfactionStates, setSatisfactionStates] = useState<{[key: number]: 'pending' | 'satisfied' | 'not-satisfied' | 'refined'}>({});
  const [refinementMode, setRefinementMode] = useState(false);
  const [originalMessageForRefinement, setOriginalMessageForRefinement] = useState('');
  
  const titleText = 'Hey there, I am Eir!';
  const subtitleText = 'How are you feeling today?';

  useEffect(() => {
    let currentIndex = 0;
    
    // Type the title first
    const titleInterval = setInterval(() => {
      if (currentIndex <= titleText.length) {
        setDisplayTitle(titleText.slice(0, currentIndex));
        currentIndex++;
      } else {
        clearInterval(titleInterval);
        setShowTitleCursor(false);
        
        // Start typing subtitle after a brief pause
        setTimeout(() => {
          setShowSubtitleCursor(true);
          let subtitleIndex = 0;
          const subtitleInterval = setInterval(() => {
            if (subtitleIndex <= subtitleText.length) {
              setDisplaySubtitle(subtitleText.slice(0, subtitleIndex));
              subtitleIndex++;
            } else {
              clearInterval(subtitleInterval);
              setShowSubtitleCursor(false);
              // Animation complete, trigger the closing animation
              setTimeout(() => {
                setAnimationComplete(true);
              }, 420);
            }
          }, 83);
        }, 420);
      }
    }, 125);

    return () => clearInterval(titleInterval);
  }, []);

  const handleEirChat = () => {
    // Start blob transformation for Eir chat
    setBlobTransforming(true);
    
    // After blob condenses and moves (600ms), start expansion and show chat immediately
    setTimeout(() => {
      setIsExpanding(true);
      setShowChat(true);
      // Start avatar appearance right away
      setTimeout(() => {
        setAvatarVisible(true);
      }, 100);
    }, 600);
    
    // After avatar is fully visible, show rest of chat interface
    setTimeout(() => {
      setShowChatContent(true);
      // Add initial greeting message
      setMessages([{
        role: 'assistant',
        content: 'Hello! I\'m Eir, your AI medical assistant. Please describe your symptoms in detail, and I\'ll help analyze them.'
      }]);
    }, 2400);
  };

  const handleRemedies = () => {
    // Transition to remedies section
    setIsExpanding(true);
    setTimeout(() => {
      setRemediesVisible(true);
    }, 800);
  };

  // Handle satisfaction feedback
  const handleSatisfaction = (messageIndex: number, satisfied: boolean) => {
    setSatisfactionStates(prev => ({
      ...prev,
      [messageIndex]: satisfied ? 'satisfied' : 'not-satisfied'
    }));
    
    if (!satisfied) {
      setRefinementMode(true);
      // Find the original user message for this AI response
      const originalUserMessage = messages[messageIndex - 1]?.content || '';
      setOriginalMessageForRefinement(originalUserMessage);
    }
  };

  // Handle refinement submission
  const handleRefinement = async (refinementText: string) => {
    if (!refinementText.trim()) return;
    
    // Add refinement message
    setMessages(prev => [...prev, { 
      role: 'user', 
      content: `Refinement: ${refinementText}` 
    }]);
    setIsLoading(true);
    setRefinementMode(false);

    try {
      // Mock API call for refinement
      await new Promise(resolve => setTimeout(resolve, 2000));
      
      // Mock refined response
      const mockRefinedResponse = {
        "query": `Original: ${originalMessageForRefinement}\nRefinement: ${refinementText}`,
        "response": {
          "Key Symptoms & Causes": [
            "Based on your additional feedback, I can provide a more targeted analysis.",
            "The refinement helps me understand your specific concerns better."
          ],
          "Home Remedies & Lifestyle Tips": [
            "Here's a more personalized approach based on your feedback.",
            "Consider these refined recommendations for your specific situation."
          ],
          "Doctor's Recommendations": [
            "With this additional information, here are more specific medical guidance.",
            "The refined analysis provides better targeted care recommendations."
          ],
          "Summary": "Thank you for the feedback! This refined response should better address your specific concerns. The analysis has been updated based on your additional input."
        }
      };
      
      const formattedResponse = formatModelResponse(mockRefinedResponse);
      
      setMessages(prev => [...prev, {
        role: 'assistant',
        content: formattedResponse
      }]);
      
      // Mark the original message as refined
      const originalMessageIndex = messages.length - 1;
      setSatisfactionStates(prev => ({
        ...prev,
        [originalMessageIndex]: 'refined'
      }));
      
    } catch (error) {
      setMessages(prev => [...prev, {
        role: 'assistant',
        content: 'I apologize, but I encountered an error processing your refinement. Please try again.'
      }]);
    } finally {
      setIsLoading(false);
    }
  };

  // All remedies data
  const allRemedies = [
    { id: 1, ailment: "Common Cold", remedy: "Honey Ginger Tea", ingredients: "1 tsp honey, 1 tsp grated ginger, 1 cup hot water", instructions: "Mix and sip slowly twice a day.", caution: "Avoid for children under 1 year (honey risk).", note: "Boosts immunity and soothes throat.", icon: "🍯" },
    { id: 2, ailment: "Cough", remedy: "Turmeric Milk", ingredients: "1 cup warm milk, 1/2 tsp turmeric powder", instructions: "Drink before bedtime.", caution: "Avoid if lactose intolerant.", note: "Reduces throat irritation and helps sleep.", icon: "🥛" },
    { id: 3, ailment: "Headache", remedy: "Peppermint Oil Massage", ingredients: "Few drops of peppermint oil, carrier oil", instructions: "Massage temples and forehead for 5 minutes.", caution: "Avoid contact with eyes.", note: "Gives cooling relief from tension headaches.", icon: "🌿" },
    { id: 4, ailment: "Fever", remedy: "Tulsi (Basil) Tea", ingredients: "10 basil leaves, 1 cup water, 1 tsp honey", instructions: "Boil leaves in water, add honey, drink warm twice daily.", caution: "Avoid honey for infants.", note: "Supports immunity and helps reduce fever.", icon: "🌿" },
    { id: 5, ailment: "Acidity", remedy: "Cumin Water", ingredients: "1 tsp cumin seeds, 1 glass water", instructions: "Boil seeds in water, cool, and drink after meals.", caution: "Avoid overuse (may lower blood sugar).", note: "Aids digestion and reduces acid reflux.", icon: "🌱" },
    { id: 6, ailment: "Indigestion", remedy: "Ginger-Lemon Mix", ingredients: "1 tsp grated ginger, few drops lemon juice", instructions: "Mix and consume after meals.", caution: "Avoid on empty stomach.", note: "Promotes digestion and reduces bloating.", icon: "🍋" },
    { id: 7, ailment: "Sore Throat", remedy: "Salt Water Gargle", ingredients: "1/2 tsp salt, 1 glass warm water", instructions: "Gargle twice daily.", caution: "Do not swallow the water.", note: "Reduces throat pain and inflammation.", icon: "🧂" },
    { id: 8, ailment: "Constipation", remedy: "Flaxseed Drink", ingredients: "1 tbsp flaxseeds, 1 glass warm water", instructions: "Soak seeds overnight and drink in the morning.", caution: "Drink plenty of water to avoid bloating.", note: "Improves bowel movement naturally.", icon: "🌾" },
    { id: 9, ailment: "Pimples / Acne", remedy: "Aloe Vera Gel", ingredients: "Fresh aloe vera gel", instructions: "Apply to affected area, leave for 20 mins, rinse.", caution: "Do patch test to avoid irritation.", note: "Soothes skin and reduces acne.", icon: "🌱" },
    { id: 10, ailment: "Muscle Pain", remedy: "Epsom Salt Bath", ingredients: "1 cup Epsom salt, warm bath water", instructions: "Soak for 15–20 minutes.", caution: "Avoid for open wounds or skin infections.", note: "Relaxes muscles and reduces soreness.", icon: "🛁" },
    { id: 11, ailment: "Hair Fall", remedy: "Coconut Oil Massage", ingredients: "2 tbsp coconut oil", instructions: "Warm oil and massage scalp twice a week.", caution: "Avoid if scalp is oily or has dandruff.", note: "Nourishes roots and strengthens hair.", icon: "🥥" },
    { id: 12, ailment: "Dry Skin", remedy: "Olive Oil Moisturizer", ingredients: "Few drops of olive oil", instructions: "Apply on dry skin before bed.", caution: "Avoid excessive use on oily skin.", note: "Keeps skin soft and hydrated.", icon: "🫒" },
    { id: 13, ailment: "Toothache", remedy: "Clove Oil Dab", ingredients: "1 drop clove oil, cotton ball", instructions: "Apply gently on affected tooth.", caution: "Do not swallow oil.", note: "Acts as natural pain reliever.", icon: "🦷" },
    { id: 14, ailment: "Nausea", remedy: "Lemon-Ginger Tea", ingredients: "1 tsp grated ginger, few drops lemon, 1 cup hot water", instructions: "Sip slowly.", caution: "Avoid excess ginger if pregnant.", note: "Calms stomach and reduces nausea.", icon: "🍋" },
    { id: 15, ailment: "Fatigue", remedy: "Banana Almond Smoothie", ingredients: "1 banana, 5 almonds, 1 cup milk", instructions: "Blend and drink chilled.", caution: "Avoid if nut allergy.", note: "Boosts energy and nutrients.", icon: "🍌" },
    { id: 16, ailment: "Sunburn", remedy: "Aloe Vera Gel", ingredients: "Fresh aloe vera gel", instructions: "Apply on affected area twice daily.", caution: "Avoid direct sunlight after application.", note: "Cools and heals sunburned skin.", icon: "☀️" }
  ];

  // Filter remedies based on search term using useMemo
  const filteredRemedies = useMemo(() => {
    if (!remedySearchTerm.trim()) return allRemedies;
    
    return allRemedies.filter(remedy => 
      remedy.ailment.toLowerCase().includes(remedySearchTerm.toLowerCase()) ||
      remedy.remedy.toLowerCase().includes(remedySearchTerm.toLowerCase()) ||
      remedy.ingredients.toLowerCase().includes(remedySearchTerm.toLowerCase()) ||
      remedy.note.toLowerCase().includes(remedySearchTerm.toLowerCase())
    );
  }, [remedySearchTerm]);

  // Function to format model response into natural conversation
  const formatModelResponse = (modelResponse: any) => {
    const { response } = modelResponse;
    
    let formattedResponse = "I understand you're experiencing some symptoms. Let me help you with some insights:\n\n";
    
    // Key Symptoms & Causes
    if (response["Key Symptoms & Causes"] && response["Key Symptoms & Causes"].length > 0) {
      formattedResponse += "**🔍 What might be happening:**\n";
      response["Key Symptoms & Causes"].forEach((point: string, index: number) => {
        formattedResponse += `📋 ${point}\n`;
      });
      formattedResponse += "\n";
    }
    
    // Home Remedies & Lifestyle Tips
    if (response["Home Remedies & Lifestyle Tips"] && response["Home Remedies & Lifestyle Tips"].length > 0) {
      formattedResponse += "**🏠 Here's what you can try at home:**\n";
      response["Home Remedies & Lifestyle Tips"].forEach((point: string, index: number) => {
        formattedResponse += `💡 ${point}\n`;
      });
      formattedResponse += "\n";
    }
    
    // Doctor's Recommendations
    if (response["Doctor's Recommendations"] && response["Doctor's Recommendations"].length > 0) {
      formattedResponse += "**🏥 When to seek medical care:**\n";
      response["Doctor's Recommendations"].forEach((point: string, index: number) => {
        formattedResponse += `⚠️ ${point}\n`;
      });
      formattedResponse += "\n";
    }
    
    // Summary
    if (response["Summary"]) {
      formattedResponse += `\n${response["Summary"]}`;
    }
    
    return formattedResponse;
  };

  const handleSendMessage = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!inputMessage.trim() || isLoading) return;

    const userMessage = inputMessage.trim();
    setInputMessage('');
    
    // Add user message
    setMessages(prev => [...prev, { role: 'user', content: userMessage }]);
    setIsLoading(true);

    try {
      // Mock API call - replace with actual model API later
      await new Promise(resolve => setTimeout(resolve, 2000));
      
      // Mock response using your model format
      const mockModelResponse = {
        "query": userMessage,
        "response": {
          "Key Symptoms & Causes": [
            "Based on your symptoms, this could be related to several common conditions.",
            "The symptoms you're describing are often associated with digestive or nervous system issues.",
            "These symptoms typically indicate irritation or inflammation in the affected area."
          ],
          "Home Remedies & Lifestyle Tips": [
            "Try drinking clear fluids and getting plenty of rest.",
            "Avoid spicy or heavy foods that might aggravate your condition.",
            "Consider gentle breathing exercises or meditation to help with any anxiety.",
            "Apply a warm compress to help soothe any discomfort."
          ],
          "Doctor's Recommendations": [
            "Monitor your symptoms and note any changes in severity.",
            "Seek medical attention if symptoms worsen or persist beyond 48 hours.",
            "Contact a healthcare provider if you experience severe pain or dehydration.",
            "Keep a symptom diary to track patterns and triggers."
          ],
          "Summary": "Your symptoms are being analyzed through our multi-model diagnostic system. While this is a mock response, your actual AI models will provide detailed medical insights. Remember to consult with a healthcare professional for proper diagnosis and treatment."
        }
      };
      
      // Format the response into natural conversation
      const formattedResponse = formatModelResponse(mockModelResponse);
      
      setMessages(prev => [...prev, {
        role: 'assistant',
        content: formattedResponse
      }]);
    } catch (error) {
      setMessages(prev => [...prev, {
        role: 'assistant',
        content: 'I apologize, but I encountered an error processing your request. Please try again.'
      }]);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-black relative overflow-hidden">
      {/* EIR Logo - Home button */}
      <div 
        className="absolute top-8 left-8 z-50 flex items-center gap-3 cursor-pointer group"
        onClick={() => {
          // Reset to home state
          setShowChat(false);
          setShowChatContent(false);
          setRemediesVisible(false);
          setShowButtonOptions(false);
          setMessages([]);
          setInputMessage('');
          setAvatarVisible(false);
          setIsExpanding(false);
          setBlobTransforming(false);
          setRemedySearchTerm('');
          
          // Reset animations for fresh start
          setAnimationComplete(false);
          setTimeout(() => {
            setAnimationComplete(true);
          }, 3000);
        }}
      >
        <div className="bg-gray-400/30 backdrop-blur-sm rounded-full p-1 shadow-lg group-hover:scale-110 transition-transform duration-300">
          <img 
            src="/logo.png" 
            alt="EIR Logo" 
            className="h-10 w-auto object-contain animate-spin-slow"
          />
        </div>
        <div className="text-white font-bold text-lg tracking-wider bg-gradient-to-r from-purple-400 via-purple-500 to-purple-600 bg-clip-text text-transparent group-hover:scale-105 transition-transform duration-300">
          EIR AI
        </div>
      </div>
      {/* Animated gradient blobs */}
      <div className="absolute inset-0">
        {/* Blob 1 - Purple - Top Left - Transforms into Eir */}
        <div 
          className={`absolute w-96 h-96 bg-purple-500/30 rounded-full mix-blend-screen filter ${
            blobTransforming 
              ? 'top-[calc(50%-16rem)] left-1/2 -translate-x-1/2 !w-32 !h-32 blur-xl scale-100 opacity-100 transition-all duration-700 ease-in-out' 
              : 'top-[10%] left-[5%] blur-3xl'
          }`}
          style={blobTransforming ? {} : { 
            animationName: 'blob',
            animationDuration: '4s',
            animationIterationCount: 'infinite',
            animationTimingFunction: 'ease-in-out',
            animationDelay: '0s'
          }}
        ></div>
        
        {/* Blob 2 - Blue - Top Right */}
        <div 
          className={`absolute top-[15%] right-[10%] w-96 h-96 bg-blue-500/30 rounded-full mix-blend-screen filter blur-3xl transition-opacity duration-700 ${blobTransforming ? 'opacity-0' : 'opacity-100'}`}
          style={blobTransforming ? {} : { 
            animationName: 'blob',
            animationDuration: '4s',
            animationIterationCount: 'infinite',
            animationTimingFunction: 'ease-in-out',
            animationDelay: '2s'
          }}
        ></div>
        
        {/* Blob 3 - Pink - Bottom Left */}
        <div 
          className={`absolute bottom-[10%] left-[15%] w-96 h-96 bg-pink-500/30 rounded-full mix-blend-screen filter blur-3xl transition-opacity duration-700 ${blobTransforming ? 'opacity-0' : 'opacity-100'}`}
          style={blobTransforming ? {} : { 
            animationName: 'blob',
            animationDuration: '4s',
            animationIterationCount: 'infinite',
            animationTimingFunction: 'ease-in-out',
            animationDelay: '4s'
          }}
        ></div>
        
        {/* Blob 4 - Cyan - Center */}
        <div 
          className={`absolute top-[45%] left-[45%] w-96 h-96 bg-cyan-500/30 rounded-full mix-blend-screen filter blur-3xl transition-opacity duration-700 ${blobTransforming ? 'opacity-0' : 'opacity-100'}`}
          style={blobTransforming ? {} : { 
            animationName: 'blob',
            animationDuration: '4s',
            animationIterationCount: 'infinite',
            animationTimingFunction: 'ease-in-out',
            animationDelay: '6s'
          }}
        ></div>
        
        {/* Blob 5 - Indigo - Bottom Right */}
        <div 
          className={`absolute bottom-[15%] right-[5%] w-96 h-96 bg-indigo-500/30 rounded-full mix-blend-screen filter blur-3xl transition-opacity duration-700 ${blobTransforming ? 'opacity-0' : 'opacity-100'}`}
          style={blobTransforming ? {} : { 
            animationName: 'blob',
            animationDuration: '4s',
            animationIterationCount: 'infinite',
            animationTimingFunction: 'ease-in-out',
            animationDelay: '8s'
          }}
        ></div>
      </div>

      {/* Title Screen with Typing Animation */}
      {!showChat && (
        <div className="absolute inset-0 z-20 flex flex-col items-center justify-center transition-all duration-1000">
          <div className={`flex flex-col items-center transition-all duration-1000 ease-out ${animationComplete ? 'gap-3' : 'gap-6'} ${isExpanding ? 'opacity-0' : 'opacity-100'}`}>
            <h1 className="font-bold text-white text-6xl md:text-8xl">
              {displayTitle}
              {showTitleCursor && <span className="animate-pulse">|</span>}
            </h1>
            <p className="text-white/80 text-2xl md:text-3xl">
              {displaySubtitle}
              {showSubtitleCursor && <span className="animate-pulse">|</span>}
            </p>
            
            {/* Elegant Button with Text */}
            {animationComplete && !isExpanding && (
              <div className="relative mt-12">
                {/* Main button */}
                <button
                  onMouseEnter={() => setShowButtonOptions(true)}
                  className="group relative overflow-hidden bg-purple-900/30 backdrop-blur-md border border-purple-500/40 hover:bg-purple-900/50 text-white rounded-full px-8 py-4 transition-all duration-500 hover:scale-105 hover:shadow-2xl hover:shadow-purple-600/50 hover:border-purple-400/60 z-30 flex items-center gap-3"
                >
                  {/* Animated background shimmer */}
                  <div className="absolute inset-0 bg-gradient-to-r from-transparent via-white/10 to-transparent -translate-x-full group-hover:translate-x-full transition-transform duration-1000"></div>
                  
                  {/* Text */}
                  <span className="relative text-lg font-semibold tracking-wide">Let's go</span>
                  
                  {/* Arrow with bounce animation */}
                  <svg 
                    xmlns="http://www.w3.org/2000/svg" 
                    className="relative h-6 w-6 group-hover:translate-y-1 transition-transform duration-300" 
                    fill="none" 
                    viewBox="0 0 24 24" 
                    stroke="currentColor"
                  >
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2.5} d="M19 9l-7 7-7-7" />
                  </svg>
                  
                  {/* Glow ring */}
                  <div className="absolute inset-0 rounded-full border-2 border-purple-400/50 opacity-0 group-hover:opacity-100 group-hover:scale-110 transition-all duration-500"></div>
                </button>
                
                {/* Dropdown buttons - side by side with cross animation */}
                <div className={`absolute top-full left-1/2 -translate-x-1/2 mt-3 flex gap-3 transition-all duration-500 ${
                  showButtonOptions ? 'opacity-100 translate-y-0' : 'opacity-0 -translate-y-3 pointer-events-none'
                }`}>
                  <button
                    onClick={() => {
                      handleEirChat();
                      setShowButtonOptions(false);
                    }}
                    className={`w-44 bg-purple-600/20 backdrop-blur-md border border-purple-500/30 hover:bg-purple-600/30 text-white rounded-full px-5 py-2.5 transition-all duration-300 hover:scale-105 hover:shadow-lg hover:border-purple-400/50 flex items-center justify-center gap-2 ${
                      showButtonOptions ? 'translate-x-0' : '-translate-x-8'
                    }`}
                  >
                    <span className="text-sm font-medium">🤖 Eir Chat</span>
                  </button>
                  <button
                    onClick={() => {
                      handleRemedies();
                      setShowButtonOptions(false);
                    }}
                    className={`w-44 bg-blue-600/20 backdrop-blur-md border border-blue-500/30 hover:bg-blue-600/30 text-white rounded-full px-5 py-2.5 transition-all duration-300 hover:scale-105 hover:shadow-lg hover:border-blue-400/50 flex items-center justify-center gap-2 ${
                      showButtonOptions ? 'translate-x-0' : 'translate-x-8'
                    }`}
                  >
                    <span className="text-sm font-medium">💊 Quick Remedies</span>
                  </button>
                </div>
              </div>
            )}
          </div>
          
          {/* Expanding overlay - Black instead of purple */}
          {isExpanding && (
            <div className="absolute inset-0 bg-black animate-expand z-25"></div>
          )}
        </div>
      )}

      {/* Remedies Section */}
      {remediesVisible && (
        <div className="absolute inset-0 z-30 bg-black flex flex-col items-center justify-center p-8">
          {/* Animated gradient background */}
          <div className="absolute inset-0">
            <div className="absolute top-0 left-1/4 w-[500px] h-[500px] bg-green-700/20 rounded-full mix-blend-screen filter blur-3xl animate-float-slow"></div>
            <div className="absolute bottom-0 right-1/4 w-[500px] h-[500px] bg-blue-700/20 rounded-full mix-blend-screen filter blur-3xl animate-float-slower"></div>
            <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[500px] h-[500px] bg-emerald-700/15 rounded-full mix-blend-screen filter blur-3xl animate-float-slowest"></div>
          </div>
          
          <div className="w-full max-w-7xl h-full flex flex-col">
            {/* Header */}
            <div className="text-center mb-8">
              <h1 className="text-4xl font-bold text-white mb-2 bg-gradient-to-r from-green-400 to-blue-500 bg-clip-text text-transparent">
                Quick Home Remedies
              </h1>
              <p className="text-gray-300 text-lg mb-6">Natural solutions for common ailments</p>
              
              {/* Search Bar */}
              <div className="max-w-2xl mx-auto">
                <div className="relative">
                  <input
                    type="text"
                    placeholder="Search for a problem or remedy (e.g., headache, cold, skin...)"
                    value={remedySearchTerm}
                    onChange={(e) => setRemedySearchTerm(e.target.value)}
                    className="w-full bg-gray-800/50 border border-green-500/30 rounded-full px-6 py-4 text-white placeholder-green-400/70 focus:outline-none focus:border-green-400 focus:ring-2 focus:ring-green-500/50 transition-all duration-300 text-center"
                  />
                  <div className="absolute right-4 top-1/2 -translate-y-1/2">
                    <svg className="w-5 h-5 text-green-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
                    </svg>
                  </div>
                </div>
                {remedySearchTerm && (
                  <p className="text-green-400/70 text-sm mt-2">
                    Found {filteredRemedies.length} remedy{filteredRemedies.length !== 1 ? 'ies' : ''} for "{remedySearchTerm}"
                  </p>
                )}
              </div>
            </div>

            {/* Remedies Grid */}
            <div className="flex-1 overflow-y-auto px-4">
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
                {filteredRemedies.length > 0 ? (
                  filteredRemedies.map((remedy) => (
                    <div key={remedy.id} className="bg-gray-800/40 backdrop-blur-sm border border-gray-700/50 rounded-2xl p-6 hover:bg-gray-700/50 transition-all duration-300 hover:scale-105 hover:shadow-xl hover:border-green-500/30">
                      <div className="flex items-start gap-4">
                        <div className="text-3xl">{remedy.icon}</div>
                        <div className="flex-1">
                          <h3 className="text-xl font-bold text-white mb-1">{remedy.ailment}</h3>
                          <p className="text-green-400 font-medium mb-2">{remedy.remedy}</p>
                          <div className="space-y-2 text-sm">
                            <div>
                              <span className="text-gray-400 font-medium">Ingredients:</span>
                              <p className="text-gray-300">{remedy.ingredients}</p>
                            </div>
                            <div>
                              <span className="text-gray-400 font-medium">Instructions:</span>
                              <p className="text-gray-300">{remedy.instructions}</p>
                            </div>
                            <div>
                              <span className="text-red-400 font-medium">⚠️ Caution:</span>
                              <p className="text-red-300">{remedy.caution}</p>
                            </div>
                            <div>
                              <span className="text-blue-400 font-medium">💡 Note:</span>
                              <p className="text-blue-300">{remedy.note}</p>
                            </div>
                          </div>
                        </div>
                      </div>
                    </div>
                  ))
                ) : (
                  <div className="col-span-full text-center py-12">
                    <div className="text-6xl mb-4">🔍</div>
                    <h3 className="text-2xl font-bold text-white mb-2">No remedies found</h3>
                    <p className="text-gray-400 mb-4">
                      No remedies match your search for "{remedySearchTerm}"
                    </p>
                    <p className="text-gray-500 text-sm">
                      Try searching for: headache, cold, skin, stomach, pain, etc.
                    </p>
                  </div>
                )}
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Main Content - chat window */}
      {showChat && (
        <div className="absolute inset-0 z-30 bg-black flex flex-col items-center justify-center p-8">
          {/* Subtle animated gradient background */}
          <div className="absolute inset-0">
            <div className={`absolute top-0 left-1/4 w-[600px] h-[600px] bg-purple-900/20 rounded-full mix-blend-screen filter blur-3xl transition-all duration-700 ${
              inputMessage.length > 0 ? 'animate-float-fast animate-pulse-strong scale-125' : 'animate-float-slow'
            }`}></div>
            <div className={`absolute bottom-0 right-1/4 w-[600px] h-[600px] bg-blue-900/20 rounded-full mix-blend-screen filter blur-3xl transition-all duration-700 ${
              inputMessage.length > 0 ? 'animate-float-faster animate-breathe scale-115' : 'animate-float-slower'
            }`}></div>
            <div className={`absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[600px] h-[600px] bg-cyan-900/15 rounded-full mix-blend-screen filter blur-3xl transition-all duration-700 ${
              inputMessage.length > 0 ? 'animate-float-medium animate-pulse scale-120' : 'animate-float-slowest'
            }`}></div>
          </div>
          {/* Centered Chat Container */}
          <div className="w-full max-w-5xl h-full flex flex-col">
            
            {/* AI Avatar - Breathing Circle - Born from blob */}
            <div className="flex justify-center mb-8">
              <div className={`relative transition-transform duration-500 ${inputMessage.length > 0 ? 'scale-125' : 'scale-100'}`}>
                {/* Outer glow rings - fade in after blob transforms - Dynamic colors */}
                <div className={`absolute inset-0 rounded-full blur-2xl transition-all duration-1000 delay-600 ${
                  avatarVisible ? 'opacity-100' : 'opacity-0'
                } ${
                  isLoading ? 'bg-purple-600/30 animate-pulse-strong' : 
                  inputMessage.length > 0 ? 'bg-blue-500/30 animate-breathe' : 
                  'bg-green-500/20 animate-breathe'
                }`}></div>
                <div className={`absolute inset-0 rounded-full blur-3xl transition-all duration-1000 delay-800 ${
                  avatarVisible ? 'opacity-100' : 'opacity-0'
                } ${
                  isLoading ? 'bg-purple-500/20 animate-pulse-strong' : 
                  inputMessage.length > 0 ? 'bg-blue-400/20 animate-breathe' : 
                  'bg-green-400/10 animate-breathe'
                }`}></div>
                
                {/* Main avatar circle - emerges from blob */}
                <div className={`relative w-32 h-32 rounded-full bg-gradient-to-br from-purple-600 to-purple-900 flex items-center justify-center transition-all duration-700 delay-500 ${
                  avatarVisible ? 'opacity-100 scale-100' : 'opacity-0 scale-50'
                } ${
                  avatarVisible && (isLoading ? 'animate-pulse-strong' : 'animate-breathe')
                } ${
                  isLoading ? 'shadow-2xl shadow-purple-600/50' : 
                  inputMessage.length > 0 ? 'shadow-2xl shadow-blue-500/50' : 
                  'shadow-2xl shadow-green-500/30'
                }`}>
                  <img 
                    src="/ai-icon.gif" 
                    alt="Eir AI Assistant"
                    className={`w-32 h-32 rounded-full object-cover transition-all duration-500 delay-1000 ${avatarVisible ? 'opacity-100' : 'opacity-0'} ${inputMessage.length > 0 ? 'scale-110' : 'scale-100'}`}
                  />
                  
                  {/* Pulse ring when active - Dynamic color */}
                  {(inputMessage.length > 0 || isLoading) && (
                    <div className={`absolute inset-0 rounded-full border-2 animate-ping ${
                      isLoading ? 'border-purple-400' : 'border-blue-400'
                    }`}></div>
                  )}
                </div>
              </div>
            </div>

            {/* Status Text */}
            {showChatContent && (
              <div className="text-center mb-6 transition-opacity duration-1000 opacity-0" style={{ animation: 'fadeIn 1s ease-in 0.3s forwards' }}>
                <p className="text-purple-300 text-sm">
                  {isLoading ? 'Analyzing your symptoms...' : inputMessage.length > 0 ? 'Listening...' : 'Ready to help'}
                </p>
              </div>
            )}

            {/* Messages Container - Scrollable */}
            {showChatContent && (
              <div className="flex-1 overflow-y-auto mb-6 space-y-4 px-4 transition-opacity duration-1000 opacity-0" style={{ animation: 'fadeIn 1s ease-in 0.5s forwards' }}>
              
              {/* Empty State - Example Questions */}
              {messages.length === 0 && (
                <div className="flex flex-col items-center justify-center h-full space-y-6 animate-fadeIn">
                  <div className="text-center space-y-3">
                    <p className="text-purple-300 text-lg font-medium">Try asking about:</p>
                    <div className="flex flex-wrap gap-3 justify-center max-w-2xl">
                      <button
                        onClick={() => setInputMessage("I have a persistent headache")}
                        className="px-5 py-2.5 bg-purple-900/40 hover:bg-purple-800/60 border border-purple-700/50 rounded-full text-purple-200 text-sm transition-all duration-300 hover:scale-105 hover:shadow-lg hover:shadow-purple-600/30"
                      >
                        💊 Headaches
                      </button>
                      <button
                        onClick={() => setInputMessage("I have a fever and body aches")}
                        className="px-5 py-2.5 bg-purple-900/40 hover:bg-purple-800/60 border border-purple-700/50 rounded-full text-purple-200 text-sm transition-all duration-300 hover:scale-105 hover:shadow-lg hover:shadow-purple-600/30"
                      >
                        🌡️ Fever
                      </button>
                      <button
                        onClick={() => setInputMessage("I'm feeling constantly fatigued")}
                        className="px-5 py-2.5 bg-purple-900/40 hover:bg-purple-800/60 border border-purple-700/50 rounded-full text-purple-200 text-sm transition-all duration-300 hover:scale-105 hover:shadow-lg hover:shadow-purple-600/30"
                      >
                        😴 Fatigue
                      </button>
                      <button
                        onClick={() => setInputMessage("I have a persistent cough")}
                        className="px-5 py-2.5 bg-purple-900/40 hover:bg-purple-800/60 border border-purple-700/50 rounded-full text-purple-200 text-sm transition-all duration-300 hover:scale-105 hover:shadow-lg hover:shadow-purple-600/30"
                      >
                        🤧 Cough
                      </button>
                      <button
                        onClick={() => setInputMessage("I'm experiencing stomach pain")}
                        className="px-5 py-2.5 bg-purple-900/40 hover:bg-purple-800/60 border border-purple-700/50 rounded-full text-purple-200 text-sm transition-all duration-300 hover:scale-105 hover:shadow-lg hover:shadow-purple-600/30"
                      >
                        🤕 Stomach Pain
                      </button>
                      <button
                        onClick={() => setInputMessage("I have chest discomfort")}
                        className="px-5 py-2.5 bg-purple-900/40 hover:bg-purple-800/60 border border-purple-700/50 rounded-full text-purple-200 text-sm transition-all duration-300 hover:scale-105 hover:shadow-lg hover:shadow-purple-600/30"
                      >
                        💔 Chest Pain
                      </button>
                    </div>
                  </div>
                  <p className="text-purple-400/60 text-sm">Click a suggestion or describe your symptoms below</p>
                </div>
              )}
              
              {messages.map((message, index) => (
                <div
                  key={index}
                  className={`flex ${message.role === 'user' ? 'justify-end animate-slide-in-right' : 'justify-start animate-slide-in-left'}`}
                >
                    <div
                      className={`max-w-[90%] rounded-3xl px-6 py-4 ${
                        message.role === 'user'
                          ? 'bg-gradient-to-r from-purple-600 to-purple-700 text-white shadow-lg shadow-purple-600/30'
                          : 'bg-purple-950/40 text-purple-50 border border-purple-800/30 backdrop-blur-sm'
                      }`}
                    >
                    <div className="text-base leading-relaxed whitespace-pre-line">
                      {message.content.split('\n').map((line, lineIndex) => {
                        // Handle bold text formatting (section headers)
                        if (line.startsWith('**') && line.endsWith('**')) {
                          const boldText = line.slice(2, -2);
                          return (
                            <div key={lineIndex} className="font-semibold text-purple-200 mb-3 mt-4 first:mt-0">
                              {boldText}
                            </div>
                          );
                        }
                        // Handle emoji bullet points (put them in boxes)
                        if (line.match(/^[🔍🏠🏥][📋💡⚠️]/) || line.startsWith('📋') || line.startsWith('💡') || line.startsWith('⚠️')) {
                          const emoji = line.charAt(0);
                          const text = line.slice(1).trim();
                          return (
                            <div key={lineIndex} className="mb-3">
                              <div className="bg-purple-900/30 border border-purple-700/40 rounded-xl p-4 flex items-start gap-4 hover:bg-purple-800/40 transition-colors duration-200 min-h-[80px]">
                                <div className="flex-shrink-0 w-8 h-8 bg-purple-800/50 rounded-lg flex items-center justify-center">
                                  <span className="text-lg">{emoji}</span>
                                </div>
                                <div className="flex-1">
                                  <span className="text-purple-100 leading-relaxed">{text}</span>
                                </div>
                              </div>
                            </div>
                          );
                        }
                        // Regular text (like summary)
                        return line ? (
                          <div key={lineIndex} className="mb-2 text-purple-100">
                            {line}
                          </div>
                        ) : (
                          <div key={lineIndex} className="mb-2"></div>
                        );
                      })}
                    </div>
                  </div>
                </div>
              ))}
              
              {/* Typing indicator */}
              {isLoading && (
                <div className="flex justify-start animate-fadeIn">
                  <div className="bg-purple-950/40 border border-purple-800/30 backdrop-blur-sm rounded-3xl px-6 py-4">
                    <div className="flex gap-2 items-center">
                      <div className="w-3 h-3 bg-purple-400 rounded-full animate-bounce"></div>
                      <div className="w-3 h-3 bg-purple-400 rounded-full animate-bounce" style={{ animationDelay: '0.2s' }}></div>
                      <div className="w-3 h-3 bg-purple-400 rounded-full animate-bounce" style={{ animationDelay: '0.4s' }}></div>
                    </div>
                  </div>
                </div>
              )}
            </div>
            )}

            {/* Input Area - Floating */}
            {showChatContent && (
            <div className="relative bg-black/95 backdrop-blur-sm -mx-8 px-8 py-6 border-t border-purple-900/20 transition-opacity duration-1000 opacity-0" style={{ animation: 'fadeIn 1s ease-in 0.7s forwards' }}>
              <form onSubmit={handleSendMessage} className="flex gap-3 items-center max-w-5xl mx-auto">
                <div className="flex-1 relative">
                  <input
                    type="text"
                    value={inputMessage}
                    onChange={(e) => setInputMessage(e.target.value)}
                    placeholder="Describe your symptoms..."
                    className="w-full bg-black border border-purple-900/50 rounded-full px-8 py-4 text-white placeholder-purple-500 focus:outline-none focus:border-purple-700 focus:ring-2 focus:ring-purple-800/50 transition-all duration-300"
                    disabled={isLoading}
                  />
                  {inputMessage.length > 0 && (
                    <div className="absolute right-4 top-1/2 -translate-y-1/2">
                      <div className="w-2 h-2 bg-purple-400 rounded-full animate-pulse"></div>
                    </div>
                  )}
                </div>
                <button
                  type="submit"
                  disabled={!inputMessage.trim() || isLoading}
                  className="bg-gradient-to-r from-purple-600 to-purple-700 hover:from-purple-500 hover:to-purple-600 disabled:from-purple-900 disabled:to-purple-950 disabled:cursor-not-allowed text-white rounded-full p-4 font-semibold transition-all duration-300 shadow-lg shadow-purple-600/30 hover:shadow-purple-500/50 hover:scale-105 disabled:shadow-none"
                >
                  <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 19l9 2-9-18-9 18 9-2zm0 0v-8" />
                  </svg>
                </button>
              </form>
            </div>
            )}
          </div>
        </div>
      )}
    </div>
  );
}
