import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Progress } from "@/components/ui/progress";
import { Heart, Users, Target, Zap } from "lucide-react";
import { useState } from "react";
import { Link } from "react-router-dom";

const Crowdfunding = () => {
  const [selectedAmount, setSelectedAmount] = useState<number | null>(null);
  const [customAmount, setCustomAmount] = useState("");
  const [error, setError] = useState<string | null>(null);

  // Mock data - Indian Rupees
  const donationGoal = 4000000; // ₹40 Lakhs
  const currentAmount = 1950000; // ₹19.5 Lakhs
  const donorCount = 156;
  const progressPercentage = (currentAmount / donationGoal) * 100;

  const donationAmounts = [500, 1000, 2500, 5000, 10000]; // Indian Rupee amounts

  const handleDonation = () => {
    const amount = selectedAmount || parseInt(customAmount);
    if (!amount || amount <= 0) {
      setError("Please select or enter a valid donation amount.");
      return;
    }

    setError(null); // clear error if valid
    window.location.href = "https://buy.stripe.com/test_dRmfZg0By14rbnubWM7bW00";
  };

  return (
    <section id="crowdfunding" className="py-20 bg-gradient-subtle">
      <div className="container mx-auto px-6">
        {/* Header */}
        <div className="text-center mb-16">
          <div className="inline-flex items-center justify-center p-2 bg-primary/10 rounded-full mb-4">
            <Heart className="text-primary" size={24} />
          </div>
          <h2 className="text-4xl md:text-5xl font-bold text-foreground mb-6">
            Help Save Lives with
            <span className="text-primary"> Thalassemia</span>
          </h2>
          <p className="text-xl text-muted-foreground max-w-3xl mx-auto leading-relaxed">
            Your donation directly supports thalassemia patients by funding blood transfusions, 
            medical equipment, and life-saving treatments. Every contribution makes a difference.
          </p>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-12 items-start">
          {/* Left Side - Campaign Info */}
          <div className="space-y-8">
            {/* Progress Card */}
            <Card className="border-primary/20 shadow-soft">
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <Target className="text-primary" size={24} />
                  Campaign Progress
                </CardTitle>
                <CardDescription>
                  Help us reach our goal to support thalassemia patients
                </CardDescription>
              </CardHeader>
              <CardContent className="space-y-6">
                <div>
                  <div className="flex justify-between items-center mb-2">
                    <span className="text-2xl font-bold text-primary">
                      ₹{currentAmount.toLocaleString("en-IN")}
                    </span>
                    <span className="text-muted-foreground">
                      of ₹{donationGoal.toLocaleString("en-IN")} goal
                    </span>
                  </div>
                  <Progress value={progressPercentage} className="h-3" />
                  <p className="text-sm text-muted-foreground mt-2">
                    {progressPercentage.toFixed(1)}% funded
                  </p>
                </div>
                
                <div className="grid grid-cols-2 gap-4">
                  <div className="text-center p-4 bg-background/50 rounded-lg">
                    <Users className="text-primary mx-auto mb-2" size={24} />
                    <div className="text-2xl font-bold text-foreground">{donorCount}</div>
                    <div className="text-sm text-muted-foreground">Donors</div>
                  </div>
                  <div className="text-center p-4 bg-background/50 rounded-lg">
                    <Zap className="text-primary mx-auto mb-2" size={24} />
                    <div className="text-2xl font-bold text-foreground">42</div>
                    <div className="text-sm text-muted-foreground">Lives Helped</div>
                  </div>
                </div>
              </CardContent>
            </Card>

            {/* Impact Information */}
            <Card className="border-primary/20 shadow-soft">
              <CardHeader>
                <CardTitle>Your Impact</CardTitle>
                <CardDescription>See how your donation helps</CardDescription>
              </CardHeader>
              <CardContent className="space-y-4">
                <div className="flex items-center gap-3 p-3 bg-primary/5 rounded-lg">
                  <Heart className="text-primary flex-shrink-0" size={20} />
                  <div>
                    <div className="font-semibold">₹500 - Emergency Support</div>
                    <div className="text-sm text-muted-foreground">
                      Provides emergency medication for one patient
                    </div>
                  </div>
                </div>
                <div className="flex items-center gap-3 p-3 bg-primary/5 rounded-lg">
                  <Heart className="text-primary flex-shrink-0" size={20} />
                  <div>
                    <div className="font-semibold">₹2,500 - Blood Transfusion</div>
                    <div className="text-sm text-muted-foreground">
                      Covers one complete blood transfusion procedure
                    </div>
                  </div>
                </div>
                <div className="flex items-center gap-3 p-3 bg-primary/5 rounded-lg">
                  <Heart className="text-primary flex-shrink-0" size={20} />
                  <div>
                    <div className="font-semibold">₹10,000 - Monthly Treatment</div>
                    <div className="text-sm text-muted-foreground">
                      Supports a patient's complete monthly treatment plan
                    </div>
                  </div>
                </div>
              </CardContent>
            </Card>
          </div>

          {/* Right Side - Donation Form */}
          <div className="space-y-6">
            <Card className="border-primary/20 shadow-soft">
              <CardHeader>
                <CardTitle>Make a Donation</CardTitle>
                <CardDescription>
                  Choose an amount to support thalassemia patients
                </CardDescription>
              </CardHeader>
              <CardContent className="space-y-6">
                {/* Preset Amounts */}
                <div>
                  <label className="text-sm font-medium text-foreground mb-3 block">
                    Select Amount
                  </label>
                  <div className="grid grid-cols-3 gap-3">
                    {donationAmounts.map((amount) => (
                      <Button
                        key={amount}
                        variant={selectedAmount === amount ? "default" : "outline"}
                        className="h-12"
                        onClick={() => {
                          setSelectedAmount(amount);
                          setCustomAmount("");
                          setError(null);
                        }}
                      >
                        ₹{amount.toLocaleString("en-IN")}
                      </Button>
                    ))}
                  </div>
                </div>

                {/* Custom Amount */}
                <div>
                  <label className="text-sm font-medium text-foreground mb-2 block">
                    Or enter custom amount
                  </label>
                  <div className="relative">
                    <span className="absolute left-3 top-1/2 transform -translate-y-1/2 text-muted-foreground">
                      ₹
                    </span>
                    <input
                      type="number"
                      placeholder="0"
                      className="w-full pl-8 pr-4 py-3 border border-input rounded-md bg-background text-foreground placeholder:text-muted-foreground focus:outline-none focus:ring-2 focus:ring-ring focus:border-transparent"
                      value={customAmount}
                      onChange={(e) => {
                        setCustomAmount(e.target.value);
                        setSelectedAmount(null);
                        setError(null);
                      }}
                      min="1"
                    />
                  </div>
                </div>

                {/* Validation error */}
                {error && <p className="text-red-500 text-sm">{error}</p>}

                {/* Donation Button */}
                <Button
                  onClick={handleDonation}
                  className="w-full h-12 text-lg font-semibold"
                  variant="hero"
                >
                  <Heart className="mr-2" size={20} />
                  Donate Now
                </Button>

                <p className="text-sm text-muted-foreground text-center">
                  Secure payment processing • No registration required
                </p>
              </CardContent>
            </Card>

            {/* Recent Donors */}
            <Card className="border-primary/20 shadow-soft">
              <CardHeader>
                <CardTitle>Recent Supporters</CardTitle>
                <CardDescription>Join these generous donors</CardDescription>
              </CardHeader>
              <CardContent>
                <div className="space-y-3">
                  {[
                    { name: "Anonymous", amount: 2500, time: "2 hours ago" },
                    { name: "Priya S.", amount: 1000, time: "5 hours ago" },
                    { name: "Anonymous", amount: 5000, time: "1 day ago" },
                    { name: "Rajesh K.", amount: 1500, time: "2 days ago" },
                  ].map((donor, index) => (
                    <div
                      key={index}
                      className="flex justify-between items-center py-2 border-b border-border/50 last:border-0"
                    >
                      <div>
                        <div className="font-medium text-foreground">{donor.name}</div>
                        <div className="text-sm text-muted-foreground">{donor.time}</div>
                      </div>
                      <div className="text-primary font-semibold">
                        ₹{donor.amount.toLocaleString("en-IN")}
                      </div>
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>
          </div>
        </div>

        {/* Bottom CTA */}
        <div className="text-center mt-16">
          <div className="max-w-2xl mx-auto">
            <h3 className="text-2xl font-bold text-foreground mb-4">
              Every Donation Counts
            </h3>
            <p className="text-muted-foreground mb-6">
              Together, we can provide hope and life-saving treatment to those fighting thalassemia. 
              Your generosity directly impacts patients in need of urgent care.
            </p>
            <Link to="/education">
              <Button
                variant="outline"
                size="lg"
                className="border-primary/30 hover:border-primary"
              >
                Learn More About Thalassemia
              </Button>
            </Link>
          </div>
        </div>
      </div>
    </section>
  );
};

export default Crowdfunding;
