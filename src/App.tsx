import React, { useState } from 'react';
import { motion, AnimatePresence } from 'motion/react';
import { Screen } from './types';

// Components
import { Navbar } from './components/Shared/Navbar';
import { BottomNav } from './components/Shared/BottomNav';
import { Dashboard } from './components/Dashboard';
import { Onboarding } from './components/Onboarding';
import { Upload } from './components/Upload';
import { Loading } from './components/Loading';
import { Analysis } from './components/Analysis';

export default function App() {
  const [screen, setScreen] = useState<Screen>('dashboard');
  const [currentEntity, setCurrentEntity] = useState<any>(null);

  const handleNavigate = (s: Screen) => setScreen(s);

  // Flow: Onboarding Complete -> Go to Upload page
  const handleOnboardingComplete = (entityData: any) => {
    setCurrentEntity(entityData);
    setScreen('upload'); // Redirect to Upload after Onboarding
  };

  // Flow: Upload/Process Complete -> Show Loading -> Show Analysis
  const handleProcessStart = () => {
    setScreen('loading');
  };

  return (
    <div className="min-h-screen bg-background-light selection:bg-primary selection:text-background-dark">
      <Navbar onNavigate={handleNavigate} />
      
      <main className="relative z-10">
        <AnimatePresence mode="wait">
          {screen === 'dashboard' && (
            <motion.div key="dashboard" initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }}>
              <Dashboard onNavigate={handleNavigate} />
            </motion.div>
          )}
          
          {screen === 'onboarding' && (
            <motion.div key="onboarding" initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }}>
              <Onboarding onNext={handleOnboardingComplete} />
            </motion.div>
          )}
          
          {screen === 'upload' && (
            <motion.div key="upload" initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }}>
              <Upload onProcess={handleProcessStart} currentEntity={currentEntity} />
            </motion.div>
          )}
          
          {screen === 'loading' && (
            <motion.div key="loading" initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }}>
              <Loading onComplete={() => setScreen('analysis')} />
            </motion.div>
          )}
          
          {screen === 'analysis' && (
            <motion.div key="analysis" initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }}>
              <Analysis currentEntity={currentEntity} />
            </motion.div>
          )}
        </AnimatePresence>
      </main>

      <BottomNav current={screen} onNavigate={handleNavigate} />

      {/* Decorative Background Elements */}
      <div className="fixed inset-0 overflow-hidden pointer-events-none z-0">
        <div className="absolute -top-20 -left-20 w-80 h-80 bg-gradient-to-br from-primary/20 to-transparent rounded-full blur-3xl animate-float"></div>
        <div className="absolute top-1/2 -right-20 w-64 h-64 bg-gradient-to-bl from-primary/10 to-transparent rounded-full blur-2xl animate-float" style={{ animationDelay: '-2s' }}></div>
        <div className="absolute bottom-1/4 -left-10 w-48 h-24 bg-primary/10 rounded-full blur-xl rotate-45 animate-float" style={{ animationDelay: '-4s' }}></div>
      </div>
    </div>
  );
}
