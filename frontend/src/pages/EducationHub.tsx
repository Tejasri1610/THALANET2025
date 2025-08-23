import { useEffect, useState } from "react";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { Badge } from "@/components/ui/badge";
import { Progress } from "@/components/ui/progress";
import { ArrowLeft, Globe, Heart, Activity, TrendingUp, Stethoscope, Users, BookOpen, Brain } from "lucide-react";
import { Link } from "react-router-dom";

const EducationHub = () => {
  const [selectedLanguage, setSelectedLanguage] = useState("en");

    useEffect(() => {
    window.scrollTo(0, 0);
  }, []);

  const languages = [
    { code: "en", name: "English", flag: "🇺🇸" },
    { code: "hi", name: "हिंदी", flag: "🇮🇳" },
    { code: "ta", name: "தமிழ்", flag: "🇮🇳" },
    { code: "te", name: "తెలుగు", flag: "🇮🇳" },
    { code: "bn", name: "বাংলা", flag: "🇧🇩" },
    { code: "ml", name: "മലയാളം", flag: "🇮🇳" },
  ];

  const content = {
    en: {
      title: "Complete Guide to Thalassemia",
      subtitle: "Understanding, treating, and living with thalassemia",
      overview: {
        title: "What is Thalassemia?",
        description: "Thalassemia is a genetic blood disorder that affects the body's ability to produce hemoglobin and red blood cells. It's one of the most common inherited disorders worldwide, particularly prevalent in Mediterranean, Middle Eastern, and South Asian populations.",
        keyPoints: [
          "Inherited genetic disorder affecting hemoglobin production",
          "More than 280 million people worldwide are carriers",
          "Requires lifelong medical management",
          "Can be effectively treated with proper care"
        ]
      },
      types: {
        title: "Types of Thalassemia",
        alpha: {
          title: "Alpha Thalassemia",
          description: "Caused by deletions in alpha globin genes on chromosome 16",
          severity: ["Silent carrier", "Alpha thalassemia trait", "Hemoglobin H disease", "Alpha thalassemia major"]
        },
        beta: {
          title: "Beta Thalassemia",
          description: "Caused by mutations in beta globin gene on chromosome 11",
          severity: ["Beta thalassemia minor", "Beta thalassemia intermedia", "Beta thalassemia major"]
        }
      },
      symptoms: {
        title: "Symptoms & Signs",
        mild: ["Mild anemia", "Fatigue", "Pale skin"],
        moderate: ["Growth delays", "Bone deformities", "Enlarged spleen"],
        severe: ["Severe anemia", "Heart problems", "Liver complications", "Iron overload"]
      },
      treatment: {
        title: "Treatment Options",
        options: [
          {
            name: "Blood Transfusions",
            description: "Regular transfusions to maintain hemoglobin levels",
            frequency: "Every 2-4 weeks for severe cases"
          },
          {
            name: "Iron Chelation",
            description: "Medications to remove excess iron from blood transfusions",
            frequency: "Daily oral or subcutaneous injection"
          },
          {
            name: "Bone Marrow Transplant",
            description: "Curative treatment for suitable patients",
            frequency: "One-time procedure with lifelong follow-up"
          },
          {
            name: "Gene Therapy",
            description: "Emerging treatment showing promising results",
            frequency: "Experimental, limited availability"
          }
        ]
      },
      statistics: {
        title: "Global Statistics",
        data: [
          { label: "Global Carriers", value: "280+ million", percentage: 4.5 },
          { label: "Annual Births Affected", value: "60,000+", percentage: 0.1 },
          { label: "Countries with High Prevalence", value: "60+", percentage: 30 },
          { label: "Survival Rate (with treatment)", value: "85%+", percentage: 85 }
        ]
      },
      forecast: {
        title: "Future Outlook & Research",
        developments: [
          {
            area: "Gene Therapy",
            progress: 75,
            description: "Clinical trials showing 80-90% success rates in β-thalassemia major patients"
          },
          {
            area: "CRISPR Gene Editing",
            progress: 60,
            description: "Promising results in laboratory studies for correcting genetic mutations"
          },
          {
            area: "Improved Chelation",
            progress: 85,
            description: "New oral iron chelators with better patient compliance"
          },
          {
            area: "Prevention Programs",
            progress: 70,
            description: "Enhanced screening and genetic counseling reducing new cases by 30%"
          }
        ]
      }
    },
    hi: {
      title: "थैलेसीमिया की संपूर्ण गाइड",
      subtitle: "थैलेसीमिया को समझना, इलाज और इसके साथ जीना",
      overview: {
        title: "थैलेसीमिया क्या है?",
        description: "थैलेसीमिया एक आनुवंशिक रक्त विकार है जो शरीर की हीमोग्लोबिन और लाल रक्त कोशिकाओं के उत्पादन की क्षमता को प्रभावित करता है। यह दुनिया भर में सबसे आम वंशानुगत विकारों में से एक है।",
        keyPoints: [
          "हीमोग्लोबिन उत्पादन को प्रभावित करने वाला आनुवंशिक विकार",
          "दुनिया भर में 280 मिलियन से अधिक लोग वाहक हैं",
          "आजीवन चिकित्सा प्रबंधन की आवश्यकता",
          "उचित देखभाल के साथ प्रभावी रूप से इलाज किया जा सकता है"
        ]
      },
      types: {
        title: "Types of Thalassemia",
        alpha: {
          title: "Alpha Thalassemia",
          description: "Caused by deletions in alpha globin genes on chromosome 16",
          severity: ["Silent carrier", "Alpha thalassemia trait", "Hemoglobin H disease", "Alpha thalassemia major"]
        },
        beta: {
          title: "Beta Thalassemia",
          description: "Caused by mutations in beta globin gene on chromosome 11",
          severity: ["Beta thalassemia minor", "Beta thalassemia intermedia", "Beta thalassemia major"]
        }
      },
      symptoms: {
        title: "Symptoms & Signs",
        mild: ["Mild anemia", "Fatigue", "Pale skin"],
        moderate: ["Growth delays", "Bone deformities", "Enlarged spleen"],
        severe: ["Severe anemia", "Heart problems", "Liver complications", "Iron overload"]
      },
      treatment: {
        title: "Treatment Options",
        options: [
          {
            name: "Blood Transfusions",
            description: "Regular transfusions to maintain hemoglobin levels",
            frequency: "Every 2-4 weeks for severe cases"
          },
          {
            name: "Iron Chelation",
            description: "Medications to remove excess iron from blood transfusions",
            frequency: "Daily oral or subcutaneous injection"
          },
          {
            name: "Bone Marrow Transplant",
            description: "Curative treatment for suitable patients",
            frequency: "One-time procedure with lifelong follow-up"
          },
          {
            name: "Gene Therapy",
            description: "Emerging treatment showing promising results",
            frequency: "Experimental, limited availability"
          }
        ]
      },
      statistics: {
        title: "Global Statistics",
        data: [
          { label: "Global Carriers", value: "280+ million", percentage: 4.5 },
          { label: "Annual Births Affected", value: "60,000+", percentage: 0.1 },
          { label: "Countries with High Prevalence", value: "60+", percentage: 30 },
          { label: "Survival Rate (with treatment)", value: "85%+", percentage: 85 }
        ]
      },
      forecast: {
        title: "Future Outlook & Research",
        developments: [
          {
            area: "Gene Therapy",
            progress: 75,
            description: "Clinical trials showing 80-90% success rates in β-thalassemia major patients"
          },
          {
            area: "CRISPR Gene Editing",
            progress: 60,
            description: "Promising results in laboratory studies for correcting genetic mutations"
          },
          {
            area: "Improved Chelation",
            progress: 85,
            description: "New oral iron chelators with better patient compliance"
          },
          {
            area: "Prevention Programs",
            progress: 70,
            description: "Enhanced screening and genetic counseling reducing new cases by 30%"
          }
        ]
      }
    }
  };

  const currentContent = content[selectedLanguage as keyof typeof content] || content.en;

  return (
    <div className="min-h-screen bg-gradient-subtle">
      {/* Header */}
      <div className="sticky top-0 z-50 bg-background/80 backdrop-blur-md border-b border-border/50">
        <div className="container mx-auto px-6 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-4">
              <Link to="/">
                <Button variant="ghost" size="sm">
                  <ArrowLeft size={16} className="mr-2" />
                  Back to Home
                </Button>
              </Link>
              <div className="h-6 w-px bg-border"></div>
              <div className="flex items-center space-x-2">
                <BookOpen className="text-primary" size={20} />
                <h1 className="text-xl font-semibold text-foreground">Education Hub</h1>
              </div>
            </div>
            
            {/* Language Selector */}
            <div className="flex items-center space-x-2">
              <Globe className="text-muted-foreground" size={16} />
              <div className="flex space-x-1">
                {languages.map((lang) => (
                  <Button
                    key={lang.code}
                    variant={selectedLanguage === lang.code ? "default" : "ghost"}
                    size="sm"
                    onClick={() => setSelectedLanguage(lang.code)}
                    className="text-xs"
                  >
                    {lang.flag} {lang.name}
                  </Button>
                ))}
              </div>
            </div>
          </div>
        </div>
      </div>

      <div className="container mx-auto px-6 py-12">
        {/* Title Section */}
        <div className="text-center mb-12">
          <h1 className="text-4xl md:text-6xl font-bold text-foreground mb-4">
            {currentContent.title}
          </h1>
          <p className="text-xl text-muted-foreground max-w-3xl mx-auto">
            {currentContent.subtitle}
          </p>
        </div>

        {/* Main Content */}
        <Tabs defaultValue="overview" className="w-full">
          <TabsList className="grid w-full grid-cols-6 mb-8">
            <TabsTrigger value="overview" className="flex items-center gap-2">
              <Heart size={16} />
              Overview
            </TabsTrigger>
            <TabsTrigger value="types" className="flex items-center gap-2">
              <Activity size={16} />
              Types
            </TabsTrigger>
            <TabsTrigger value="symptoms" className="flex items-center gap-2">
              <Stethoscope size={16} />
              Symptoms
            </TabsTrigger>
            <TabsTrigger value="treatment" className="flex items-center gap-2">
              <Brain size={16} />
              Treatment
            </TabsTrigger>
            <TabsTrigger value="statistics" className="flex items-center gap-2">
              <Users size={16} />
              Statistics
            </TabsTrigger>
            <TabsTrigger value="future" className="flex items-center gap-2">
              <TrendingUp size={16} />
              Future
            </TabsTrigger>
          </TabsList>

          {/* Overview Tab */}
          <TabsContent value="overview" className="space-y-8">
            <Card className="shadow-soft border-primary/20">
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <Heart className="text-primary" size={24} />
                  {currentContent.overview.title}
                </CardTitle>
              </CardHeader>
              <CardContent className="space-y-6">
                <p className="text-lg text-muted-foreground leading-relaxed">
                  {currentContent.overview.description}
                </p>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  {currentContent.overview.keyPoints.map((point, index) => (
                    <div key={index} className="flex items-start gap-3 p-4 bg-primary/5 rounded-lg">
                      <div className="w-2 h-2 bg-primary rounded-full mt-2 flex-shrink-0"></div>
                      <span className="text-foreground">{point}</span>
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>
          </TabsContent>

          {/* Types Tab */}
          <TabsContent value="types" className="space-y-8">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
              <Card className="shadow-soft border-primary/20">
                <CardHeader>
                  <CardTitle className="text-red-600">
                    {currentContent.types.alpha.title}
                  </CardTitle>
                  <CardDescription>
                    {currentContent.types.alpha.description}
                  </CardDescription>
                </CardHeader>
                <CardContent>
                  <div className="space-y-3">
                    <h4 className="font-semibold">Severity Levels:</h4>
                    {currentContent.types.alpha.severity.map((level, index) => (
                      <Badge key={index} variant="outline" className="mr-2 mb-2">
                        {level}
                      </Badge>
                    ))}
                  </div>
                </CardContent>
              </Card>

              <Card className="shadow-soft border-primary/20">
                <CardHeader>
                  <CardTitle className="text-blue-600">
                    {currentContent.types.beta.title}
                  </CardTitle>
                  <CardDescription>
                    {currentContent.types.beta.description}
                  </CardDescription>
                </CardHeader>
                <CardContent>
                  <div className="space-y-3">
                    <h4 className="font-semibold">Severity Levels:</h4>
                    {currentContent.types.beta.severity.map((level, index) => (
                      <Badge key={index} variant="outline" className="mr-2 mb-2">
                        {level}
                      </Badge>
                    ))}
                  </div>
                </CardContent>
              </Card>
            </div>
          </TabsContent>

          {/* Symptoms Tab */}
          <TabsContent value="symptoms" className="space-y-8">
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
              <Card className="shadow-soft border-yellow-200">
                <CardHeader>
                  <CardTitle className="text-yellow-600">Mild Symptoms</CardTitle>
                </CardHeader>
                <CardContent>
                  <ul className="space-y-2">
                    {currentContent.symptoms.mild.map((symptom, index) => (
                      <li key={index} className="flex items-center gap-2">
                        <div className="w-2 h-2 bg-yellow-500 rounded-full"></div>
                        {symptom}
                      </li>
                    ))}
                  </ul>
                </CardContent>
              </Card>

              <Card className="shadow-soft border-orange-200">
                <CardHeader>
                  <CardTitle className="text-orange-600">Moderate Symptoms</CardTitle>
                </CardHeader>
                <CardContent>
                  <ul className="space-y-2">
                    {currentContent.symptoms.moderate.map((symptom, index) => (
                      <li key={index} className="flex items-center gap-2">
                        <div className="w-2 h-2 bg-orange-500 rounded-full"></div>
                        {symptom}
                      </li>
                    ))}
                  </ul>
                </CardContent>
              </Card>

              <Card className="shadow-soft border-red-200">
                <CardHeader>
                  <CardTitle className="text-red-600">Severe Symptoms</CardTitle>
                </CardHeader>
                <CardContent>
                  <ul className="space-y-2">
                    {currentContent.symptoms.severe.map((symptom, index) => (
                      <li key={index} className="flex items-center gap-2">
                        <div className="w-2 h-2 bg-red-500 rounded-full"></div>
                        {symptom}
                      </li>
                    ))}
                  </ul>
                </CardContent>
              </Card>
            </div>
          </TabsContent>

          {/* Treatment Tab */}
          <TabsContent value="treatment" className="space-y-8">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              {currentContent.treatment.options.map((treatment, index) => (
                <Card key={index} className="shadow-soft border-primary/20">
                  <CardHeader>
                    <CardTitle className="text-primary">{treatment.name}</CardTitle>
                    <CardDescription>{treatment.frequency}</CardDescription>
                  </CardHeader>
                  <CardContent>
                    <p className="text-muted-foreground">{treatment.description}</p>
                  </CardContent>
                </Card>
              ))}
            </div>
          </TabsContent>

          {/* Statistics Tab */}
          <TabsContent value="statistics" className="space-y-8">
            <Card className="shadow-soft border-primary/20">
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <Users className="text-primary" size={24} />
                  {currentContent.statistics.title}
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                  {currentContent.statistics.data.map((stat, index) => (
                    <div key={index} className="space-y-3">
                      <div className="flex justify-between items-center">
                        <span className="font-medium">{stat.label}</span>
                        <span className="text-2xl font-bold text-primary">{stat.value}</span>
                      </div>
                      <Progress value={stat.percentage} className="h-2" />
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>
          </TabsContent>

          {/* Future Tab */}
          <TabsContent value="future" className="space-y-8">
            <Card className="shadow-soft border-primary/20">
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <TrendingUp className="text-primary" size={24} />
                  {currentContent.forecast.title}
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-6">
                  {currentContent.forecast.developments.map((dev, index) => (
                    <div key={index} className="space-y-3">
                      <div className="flex justify-between items-center">
                        <h4 className="font-semibold text-foreground">{dev.area}</h4>
                        <Badge variant="outline">{dev.progress}% Progress</Badge>
                      </div>
                      <Progress value={dev.progress} className="h-2" />
                      <p className="text-muted-foreground text-sm">{dev.description}</p>
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>
          </TabsContent>
        </Tabs>

        {/* Call to Action */}
        <div className="mt-16 text-center">
          <Card className="max-w-2xl mx-auto shadow-soft border-primary/20">
            <CardContent className="pt-6">
              <h3 className="text-2xl font-bold text-foreground mb-4">
                Need Support or Have Questions?
              </h3>
              <p className="text-muted-foreground mb-6">
                Connect with our community and healthcare professionals for guidance and support.
              </p>
              <div className="flex flex-col sm:flex-row gap-4 justify-center">
                <Link to="/">
                  <Button variant="default" size="lg">
                    <Heart className="mr-2" size={20} />
                    Support a Patient
                  </Button>
                </Link>
                <Button variant="outline" size="lg">
                  <Users className="mr-2" size={20} />
                  Join Community
                </Button>
              </div>
            </CardContent>
          </Card>
        </div>
      </div>
    </div>
  );
};

export default EducationHub;