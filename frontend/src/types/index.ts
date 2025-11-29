export interface User {
    id: string;
    email: string;
    username: string;
    full_name?: string;
    role: 'student' | 'mentor' | 'recruiter' | 'admin';
    is_verified: boolean;
    is_active: boolean;
    created_at: string;
}

export interface Profile {
    id: string;
    user_id: string;
    bio?: string;
    university?: string;
    graduation_year?: number;
    github_url?: string;
    linkedin_url?: string;
    portfolio_url?: string;
    avatar_url?: string;
    location?: string;
    reputation_score: number;
    created_at: string;
}

export interface Skill {
    id: string;
    name: string;
    category?: string;
}

export interface UserSkill {
    skill: Skill;
    proficiency_level: 'beginner' | 'intermediate' | 'advanced' | 'expert';
}

export interface Interest {
    id: string;
    name: string;
    category?: string;
}

export interface Community {
    id: string;
    name: string;
    slug: string;
    description?: string;
    category?: string;
    icon_url?: string;
    banner_url?: string;
    created_by?: string;
    member_count: number;
    is_private: boolean;
    created_at: string;
}

export interface Post {
    _id: string;
    user_id: string;
    community_id: string;
    title: string;
    content: string;
    content_type: 'discussion' | 'question' | 'showcase' | 'article';
    tags: string[];
    upvotes: number;
    downvotes: number;
    view_count: number;
    comment_count: number;
    is_pinned: boolean;
    created_at: string;
}

export interface Hackathon {
    id: string;
    title: string;
    description?: string;
    organizer?: string;
    start_date: string;
    end_date: string;
    registration_deadline?: string;
    mode: 'online' | 'offline' | 'hybrid';
    location?: string;
    prize_pool?: string;
    website_url?: string;
    banner_url?: string;
    max_team_size: number;
    min_team_size: number;
    status: 'upcoming' | 'ongoing' | 'completed';
    created_at: string;
}

export interface Team {
    id: string;
    name: string;
    description?: string;
    hackathon_id: string;
    leader_id?: string;
    max_members: number;
    current_members: number;
    is_open: boolean;
    status: 'forming' | 'complete' | 'disbanded';
    created_at: string;
}

export interface AuthTokens {
    access_token: string;
    refresh_token: string;
    token_type: string;
}

export interface LoginCredentials {
    email: string;
    password: string;
}

export interface RegisterData {
    email: string;
    username: string;
    password: string;
    full_name?: string;
}
