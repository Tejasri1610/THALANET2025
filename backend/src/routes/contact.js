import { Router } from 'express';

const router = Router();

// POST contact form
router.post('/', (req, res) => {
  const { name, email, subject, message } = req.body;
  console.log('📩 Contact form:', { name, email, subject, message });

  res.json({
    success: true,
    message: 'Message sent successfully. We’ll reply within 24 hrs.'
  });
});

export default router;
