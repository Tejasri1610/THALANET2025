// Mock API service for ThalaNet
// TODO: Replace with actual Azure backend API calls

export interface UrgentRequest {
  id: string;
  title: string;
  description: string;
  bloodType: string;
  location: string;
  requesterName: string;
  requesterPhone: string;
  hospital: string;
  expiryTime: Date;
  urgency: 'critical' | 'high' | 'medium';
  status: 'active' | 'fulfilled' | 'expired';
  createdAt: Date;
}

export interface CreateRequestData {
  title: string;
  description: string;
  bloodType: string;
  location: string;
  requesterName: string;
  requesterPhone: string;
  hospital: string;
  urgency: 'critical' | 'high' | 'medium';
  expiryHours: number;
}

export interface ContactFormData {
  name: string;
  email: string;
  phone?: string;
  subject: string;
  message: string;
  inquiryType: string;
}

// Mock data storage
let mockRequests: UrgentRequest[] = [
  {
    id: "1",
    title: "Urgent B+ Blood Required",
    description: "Patient needs immediate blood transfusion for surgery. Critical condition.",
    bloodType: "B+",
    location: "Mumbai, Maharashtra",
    requesterName: "Dr. Priya Sharma",
    requesterPhone: "+91-98765-43210",
    hospital: "Apollo Hospital",
    expiryTime: new Date(Date.now() + 2 * 60 * 60 * 1000), // 2 hours
    urgency: 'critical',
    status: 'active',
    createdAt: new Date(Date.now() - 30 * 60 * 1000) // 30 minutes ago
  },
  {
    id: "2",
    title: "A- Blood Needed for Child",
    description: "5-year-old child with thalassemia needs blood. Please help.",
    bloodType: "A-",
    location: "Delhi, NCR",
    requesterName: "Rahul Verma",
    requesterPhone: "+91-98765-43211",
    hospital: "Safdarjung Hospital",
    expiryTime: new Date(Date.now() + 24 * 60 * 60 * 1000), // 24 hours
    urgency: 'high',
    status: 'active',
    createdAt: new Date(Date.now() - 2 * 60 * 60 * 1000) // 2 hours ago
  },
  {
    id: "3",
    title: "O+ Blood Required Today",
    description: "Emergency surgery scheduled. Blood needed by evening.",
    bloodType: "O+",
    location: "Bangalore, Karnataka",
    requesterName: "Dr. Amit Patel",
    requesterPhone: "+91-98765-43212",
    hospital: "Manipal Hospital",
    expiryTime: new Date(Date.now() + 8 * 60 * 60 * 1000), // 8 hours
    urgency: 'high',
    status: 'active',
    createdAt: new Date(Date.now() - 4 * 60 * 60 * 1000) // 4 hours ago
  }
];

// Simulate API delay
const simulateApiDelay = (ms: number = 500) => new Promise(resolve => setTimeout(resolve, ms));

// Urgent Requests API
export const urgentRequestsApi = {
  // Get all urgent requests
  async getAll(): Promise<UrgentRequest[]> {
    await simulateApiDelay();
    
    // Filter out expired requests
    const now = new Date();
    mockRequests = mockRequests.filter(request => request.expiryTime > now);
    
    // Sort by urgency and time remaining
    return mockRequests.sort((a, b) => {
      const urgencyOrder = { critical: 3, high: 2, medium: 1 };
      const urgencyDiff = urgencyOrder[b.urgency] - urgencyOrder[a.urgency];
      if (urgencyDiff !== 0) return urgencyDiff;
      
      return a.expiryTime.getTime() - b.expiryTime.getTime();
    });
  },

  // Get request by ID
  async getById(id: string): Promise<UrgentRequest | null> {
    await simulateApiDelay();
    return mockRequests.find(request => request.id === id) || null;
  },

  // Create new urgent request
  async create(data: CreateRequestData): Promise<UrgentRequest> {
    await simulateApiDelay();
    
    const newRequest: UrgentRequest = {
      id: Date.now().toString(),
      ...data,
      expiryTime: new Date(Date.now() + data.expiryHours * 60 * 60 * 1000),
      status: 'active',
      createdAt: new Date()
    };
    
    mockRequests.push(newRequest);
    
    // TODO: Send notification to potential donors
    // await this.notifyPotentialDonors(newRequest);
    
    return newRequest;
  },

  // Update request status
  async updateStatus(id: string, status: 'active' | 'fulfilled' | 'expired'): Promise<UrgentRequest | null> {
    await simulateApiDelay();
    
    const requestIndex = mockRequests.findIndex(request => request.id === id);
    if (requestIndex === -1) return null;
    
    mockRequests[requestIndex].status = status;
    return mockRequests[requestIndex];
  },

  // Delete request
  async delete(id: string): Promise<boolean> {
    await simulateApiDelay();
    
    const initialLength = mockRequests.length;
    mockRequests = mockRequests.filter(request => request.id !== id);
    
    return mockRequests.length < initialLength;
  },

  // Get requests by urgency level
  async getByUrgency(urgency: 'critical' | 'high' | 'medium'): Promise<UrgentRequest[]> {
    await simulateApiDelay();
    return mockRequests.filter(request => request.urgency === urgency);
  },

  // Get requests by blood type
  async getByBloodType(bloodType: string): Promise<UrgentRequest[]> {
    await simulateApiDelay();
    return mockRequests.filter(request => request.bloodType === bloodType);
  },

  // Search requests
  async search(query: string): Promise<UrgentRequest[]> {
    await simulateApiDelay();
    
    const searchTerm = query.toLowerCase();
    return mockRequests.filter(request => 
      request.title.toLowerCase().includes(searchTerm) ||
      request.description.toLowerCase().includes(searchTerm) ||
      request.location.toLowerCase().includes(searchTerm) ||
      request.hospital.toLowerCase().includes(searchTerm)
    );
  }
};

// Contact API
export const contactApi = {
  async submit(data: ContactFormData): Promise<{ success: boolean; message: string }> {
    await simulateApiDelay();
    
    // TODO: Send email notification to support team
    // await this.sendEmailNotification(data);
    
    console.log('Contact form submitted:', data);
    
    return {
      success: true,
      message: 'Your message has been sent successfully. We\'ll get back to you within 24 hours.'
    };
  }
};

// Analytics API
export const analyticsApi = {
  async getStats(): Promise<{
    totalRequests: number;
    activeRequests: number;
    criticalRequests: number;
    fulfilledRequests: number;
    totalDonors: number;
    responseTime: number;
  }> {
    await simulateApiDelay();
    
    const now = new Date();
    const activeRequests = mockRequests.filter(request => 
      request.status === 'active' && request.expiryTime > now
    );
    
    return {
      totalRequests: mockRequests.length,
      activeRequests: activeRequests.length,
      criticalRequests: activeRequests.filter(r => r.urgency === 'critical').length,
      fulfilledRequests: mockRequests.filter(r => r.status === 'fulfilled').length,
      totalDonors: 50000, // Mock data
      responseTime: 15 // Average response time in minutes
    };
  }
};

// Notification API
export const notificationApi = {
  async sendEmergencyNotification(request: UrgentRequest): Promise<boolean> {
    await simulateApiDelay();
    
    // TODO: Implement real-time notifications
    // - Push notifications to mobile apps
    // - SMS notifications to registered donors
    // - Email notifications
    // - WhatsApp notifications
    
    console.log('Emergency notification sent for request:', request.id);
    return true;
  },

  async subscribeToNotifications(userId: string, preferences: {
    email: boolean;
    sms: boolean;
    push: boolean;
    whatsapp: boolean;
  }): Promise<boolean> {
    await simulateApiDelay();
    
    // TODO: Store user notification preferences in database
    console.log('User subscribed to notifications:', userId, preferences);
    return true;
  }
};

// Export types for use in components
export type { UrgentRequest, CreateRequestData, ContactFormData };
