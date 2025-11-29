import React from 'react';
import { Link } from 'react-router-dom';
import { motion } from 'framer-motion';
import { Code2, Users, Rocket, Sparkles, ArrowRight, Github, Linkedin, GitMerge, Search, Trophy } from 'lucide-react';

const LandingPage: React.FC = () => {
    return (
        <div className="min-h-screen bg-dark-950 relative overflow-hidden">
            {/* Animated Grid Background */}
            <div className="absolute inset-0 z-0">
                <div className="absolute inset-0 bg-[linear-gradient(to_right,#80808012_1px,transparent_1px),linear-gradient(to_bottom,#80808012_1px,transparent_1px)] bg-[size:24px_24px]"></div>
                <div className="absolute left-0 right-0 top-0 -z-10 m-auto h-[310px] w-[310px] rounded-full bg-primary-500 opacity-20 blur-[100px]"></div>
            </div>

            {/* Navigation */}
            <nav className="fixed top-0 w-full z-50 glass border-b border-white/5 backdrop-blur-md">
                <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
                    <div className="flex justify-between items-center h-16">
                        <div className="flex items-center space-x-2">
                            <div className="bg-gradient-to-tr from-primary-600 to-primary-400 p-2 rounded-lg">
                                <Code2 className="h-6 w-6 text-white" />
                            </div>
                            <span className="text-2xl font-bold text-white tracking-tight">TechKatta</span>
                        </div>
                        <div className="flex items-center space-x-4">
                            <Link to="/login" className="text-dark-200 hover:text-white transition font-medium">
                                Login
                            </Link>
                            <Link to="/register" className="btn btn-primary shadow-lg shadow-primary-500/20">
                                Get Started
                            </Link>
                        </div>
                    </div>
                </div>
            </nav>

            {/* Hero Section */}
            <section className="pt-32 pb-20 px-4 relative z-10">
                <div className="max-w-7xl mx-auto">
                    <div className="flex flex-col lg:flex-row items-center gap-12">
                        <motion.div
                            initial={{ opacity: 0, x: -20 }}
                            animate={{ opacity: 1, x: 0 }}
                            transition={{ duration: 0.6 }}
                            className="flex-1 text-center lg:text-left"
                        >
                            <div className="inline-block px-4 py-1.5 mb-6 rounded-full border border-primary-500/30 bg-primary-500/10 text-primary-300 text-sm font-medium">
                                🚀 The #1 Platform for Engineering Students
                            </div>
                            <h1 className="text-5xl md:text-7xl font-bold text-white mb-6 leading-tight">
                                Connect. Collaborate. <br />
                                <span className="text-transparent bg-clip-text bg-gradient-to-r from-primary-400 to-purple-400">
                                    Build the Future.
                                </span>
                            </h1>
                            <p className="text-xl text-dark-300 mb-8 max-w-2xl mx-auto lg:mx-0 leading-relaxed">
                                Don't code alone. Find your dream team, join hackathons, and get AI-powered recommendations to accelerate your engineering journey.
                            </p>
                            <div className="flex flex-col sm:flex-row gap-4 justify-center lg:justify-start">
                                <Link to="/register" className="btn btn-primary text-lg px-8 py-4 flex items-center justify-center gap-2 shadow-xl shadow-primary-600/20 hover:scale-105 transition-transform">
                                    Join TechKatta <ArrowRight className="h-5 w-5" />
                                </Link>
                                <button className="btn btn-outline text-lg px-8 py-4 text-white border-white/20 hover:bg-white/5 backdrop-blur-sm">
                                    View Demo
                                </button>
                            </div>
                        </motion.div>

                        {/* Floating Hero Visual */}
                        <motion.div
                            initial={{ opacity: 0, scale: 0.8 }}
                            animate={{ opacity: 1, scale: 1 }}
                            transition={{ duration: 0.8 }}
                            className="flex-1 relative"
                        >
                            <div className="relative w-full max-w-md mx-auto aspect-square">
                                <div className="absolute inset-0 bg-gradient-to-tr from-primary-600/30 to-purple-600/30 rounded-full blur-3xl animate-pulse"></div>
                                <div className="relative z-10 bg-dark-900/80 backdrop-blur-xl border border-white/10 rounded-2xl p-6 shadow-2xl transform rotate-3 hover:rotate-0 transition-transform duration-500">
                                    <div className="flex items-center gap-4 mb-6 border-b border-white/10 pb-4">
                                        <div className="h-12 w-12 rounded-full bg-gradient-to-br from-primary-500 to-purple-600 flex items-center justify-center">
                                            <Trophy className="h-6 w-6 text-white" />
                                        </div>
                                        <div>
                                            <h3 className="text-white font-bold">Hackathon Winner</h3>
                                            <p className="text-primary-400 text-sm">Team "CodeCrushers"</p>
                                        </div>
                                    </div>
                                    <div className="space-y-3">
                                        <div className="h-2 bg-dark-800 rounded-full w-3/4"></div>
                                        <div className="h-2 bg-dark-800 rounded-full w-full"></div>
                                        <div className="h-2 bg-dark-800 rounded-full w-5/6"></div>
                                    </div>
                                    <div className="mt-6 flex gap-2">
                                        <span className="px-3 py-1 rounded-full bg-primary-500/20 text-primary-300 text-xs">React</span>
                                        <span className="px-3 py-1 rounded-full bg-blue-500/20 text-blue-300 text-xs">Python</span>
                                        <span className="px-3 py-1 rounded-full bg-green-500/20 text-green-300 text-xs">AI/ML</span>
                                    </div>
                                </div>
                            </div>
                        </motion.div>
                    </div>
                </div>
            </section>

            {/* How It Works Section */}
            <section className="py-24 px-4 relative z-10">
                <div className="max-w-7xl mx-auto">
                    <div className="text-center mb-16">
                        <h2 className="text-3xl md:text-4xl font-bold text-white mb-4">How TechKatta Works</h2>
                        <p className="text-dark-400 max-w-2xl mx-auto">Three simple steps to supercharge your college experience.</p>
                    </div>
                    <div className="grid md:grid-cols-3 gap-12">
                        <StepCard
                            number="01"
                            icon={<GitMerge className="h-8 w-8" />}
                            title="Create Profile"
                            description="Import your GitHub & LinkedIn. Showcase your skills, projects, and interests to the community."
                        />
                        <StepCard
                            number="02"
                            icon={<Search className="h-8 w-8" />}
                            title="Get Matched"
                            description="Our AI algorithm finds the perfect teammates and hackathons based on your skill level."
                        />
                        <StepCard
                            number="03"
                            icon={<Rocket className="h-8 w-8" />}
                            title="Build & Win"
                            description="Collaborate in real-time, build amazing projects, and earn reputation points."
                        />
                    </div>
                </div>
            </section>

            {/* Feature Cards */}
            <section className="py-20 px-4 bg-dark-900/30">
                <div className="max-w-7xl mx-auto">
                    <motion.div
                        initial={{ opacity: 0, y: 40 }}
                        whileInView={{ opacity: 1, y: 0 }}
                        viewport={{ once: true }}
                        transition={{ duration: 0.6 }}
                        className="grid md:grid-cols-3 gap-8"
                    >
                        <FeatureCard
                            icon={<Users className="h-10 w-10" />}
                            title="Tech Communities"
                            description="Join communities based on your interests - AI, Web Dev, Mobile, IoT, and more."
                            gradient="from-blue-500 to-cyan-500"
                        />
                        <FeatureCard
                            icon={<Rocket className="h-10 w-10" />}
                            title="Find Teammates"
                            description="AI-powered matching to find the perfect teammates for your next hackathon."
                            gradient="from-purple-500 to-pink-500"
                        />
                        <FeatureCard
                            icon={<Sparkles className="h-10 w-10" />}
                            title="Smart Recommendations"
                            description="Get personalized content, learning paths, and opportunities tailored to you."
                            gradient="from-orange-500 to-red-500"
                        />
                    </motion.div>
                </div>
            </section>

            {/* Stats Section */}
            <section className="py-20 px-4 border-y border-white/5 bg-dark-900/50 backdrop-blur-sm">
                <div className="max-w-7xl mx-auto">
                    <div className="grid md:grid-cols-4 gap-8 text-center">
                        <StatCard number="10K+" label="Students" />
                        <StatCard number="500+" label="Communities" />
                        <StatCard number="1K+" label="Hackathons" />
                        <StatCard number="5K+" label="Teams Formed" />
                    </div>
                </div>
            </section>

            {/* Footer */}
            <footer className="py-12 px-4 border-t border-white/5 bg-dark-950">
                <div className="max-w-7xl mx-auto">
                    <div className="flex flex-col md:flex-row justify-between items-center">
                        <div className="flex items-center space-x-2 mb-4 md:mb-0">
                            <div className="bg-dark-800 p-1.5 rounded-lg">
                                <Code2 className="h-5 w-5 text-primary-400" />
                            </div>
                            <span className="text-xl font-bold text-white">TechKatta</span>
                        </div>
                        <div className="flex space-x-6">
                            <a href="#" className="text-dark-400 hover:text-white transition hover:scale-110 transform">
                                <Github className="h-6 w-6" />
                            </a>
                            <a href="#" className="text-dark-400 hover:text-white transition hover:scale-110 transform">
                                <Linkedin className="h-6 w-6" />
                            </a>
                        </div>
                    </div>
                    <div className="mt-8 text-center text-dark-500 text-sm">
                        © 2024 TechKatta. Built for engineers, by engineers.
                    </div>
                </div>
            </footer>
        </div>
    );
};

const FeatureCard: React.FC<{
    icon: React.ReactNode;
    title: string;
    description: string;
    gradient: string;
}> = ({ icon, title, description, gradient }) => {
    return (
        <motion.div
            whileHover={{ y: -5 }}
            className="p-8 rounded-2xl bg-dark-900/50 border border-white/5 hover:border-primary-500/30 transition-all duration-300 group"
        >
            <div className={`inline-flex p-3 rounded-xl bg-gradient-to-br ${gradient} mb-6 shadow-lg`}>
                <div className="text-white">{icon}</div>
            </div>
            <h3 className="text-xl font-bold text-white mb-3 group-hover:text-primary-400 transition-colors">{title}</h3>
            <p className="text-dark-400 leading-relaxed">{description}</p>
        </motion.div>
    );
};

const StepCard: React.FC<{
    number: string;
    icon: React.ReactNode;
    title: string;
    description: string;
}> = ({ number, icon, title, description }) => {
    return (
        <Link to="/register" className="block relative p-6 rounded-2xl bg-white/5 border border-white/5 hover:bg-white/10 transition-colors group">
            <div className="absolute -top-4 -left-4 w-10 h-10 rounded-full bg-dark-950 border border-primary-500 flex items-center justify-center text-primary-400 font-bold group-hover:scale-110 transition-transform">
                {number}
            </div>
            <div className="mb-4 text-primary-400 group-hover:text-primary-300 transition-colors">{icon}</div>
            <h3 className="text-xl font-bold text-white mb-2">{title}</h3>
            <p className="text-dark-400">{description}</p>
        </Link>
    );
};

const StatCard: React.FC<{ number: string; label: string }> = ({ number, label }) => {
    return (
        <div>
            <div className="text-4xl md:text-5xl font-bold text-transparent bg-clip-text bg-gradient-to-b from-white to-dark-400 mb-2">{number}</div>
            <div className="text-primary-400 font-medium">{label}</div>
        </div>
    );
};

export default LandingPage;
