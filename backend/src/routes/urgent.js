import { Router } from 'express';

const router = Router();

// GET urgent blood requests
router.get('/', (req, res) => {
  res.json([
    {
      id: "1",
      title: "Urgent B+ Blood Required",
      description: "Patient needs immediate blood transfusion for surgery.",
      bloodType: "B+",
      location: "Mumbai, Maharashtra",
      requesterName: "Dr. Priya Sharma",
      requesterPhone: "+91-98765-43210",
      hospital: "Apollo Hospital",
      expiryTime: new Date(Date.now() + 2 * 60 * 60 * 1000).toISOString(),
      urgency: 'critical',
      status: 'active',
      createdAt: new Date(Date.now() - 30 * 60 * 1000).toISOString()
    }
  ]);
});

export default router;
