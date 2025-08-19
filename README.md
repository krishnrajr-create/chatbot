# 🚚 FastShip Courier - AI-Powered Chatbot

A modern, interactive courier service website with an AI-powered chatbot assistant built with Flask, Groq AI, and a beautiful responsive frontend.

## ✨ Features

### 🤖 AI Chatbot Assistant
- **Intelligent Responses**: Powered by Groq's Llama3-8b model
- **Context-Aware**: Maintains conversation history for better interactions
- **Courier Expertise**: Specialized in package tracking, delivery schedules, pricing, and customer support
- **Auto-Open**: Chatbot automatically opens with a pleasant pop sound when the website loads
- **Circular Design**: Modern floating chatbot button with robot icon

### 💰 Interactive Pricing Estimator
- **Real-time Calculations**: Instant price estimates based on distance, weight, and service speed
- **Transparent Pricing**: Shows detailed breakdown of costs
- **Multiple Service Tiers**: Standard, Express, and Same-day delivery options
- **User-Friendly Interface**: Clean form with immediate results

### 🎨 Modern UI/UX
- **Responsive Design**: Works perfectly on desktop, tablet, and mobile
- **Interactive Elements**: Hover effects, smooth animations, and scroll-triggered reveals
- **Courier-Themed Images**: Professional courier and delivery imagery
- **Beautiful Typography**: Google Fonts integration with Roboto
- **Gradient Headers**: Eye-catching purple gradient design

### 📱 Multi-Page Website
- **Home Page**: Hero section with CTA, services overview, and image gallery
- **Services Page**: Detailed service offerings
- **Pricing Page**: Interactive estimator and pricing information
- **Contact Page**: Contact form for customer inquiries

## 🛠️ Technologies Used

### Backend
- **Flask 2.3.3**: Python web framework
- **Groq AI**: LLM API for intelligent chatbot responses
- **Python-dotenv**: Environment variable management
- **Session Management**: Flask sessions for chat history

### Frontend
- **HTML5**: Semantic markup
- **CSS3**: Modern styling with Flexbox and Grid
- **JavaScript (ES6+)**: Interactive features and API calls
- **Google Fonts**: Roboto font family
- **Web Audio API**: Custom pop sound effects

### Deployment
- **Vercel**: Serverless deployment platform
- **Environment Variables**: Secure API key management
- **Static Asset Optimization**: Optimized for performance

## 🚀 Quick Start

### Prerequisites
- Python 3.9 or higher
- Groq API key (get one at [groq.com](https://groq.com))

### Local Development Setup

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd chatbot
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   ```bash
   # Create .env file
   echo "GROQ_API_KEY=your_groq_api_key_here" > .env
   ```

5. **Run the application**
   ```bash
   python app.py
   ```

6. **Open your browser**
   Navigate to `http://localhost:5000`

## 🌐 Deployment to Vercel

### 1. Prepare Your Repository
Ensure your repository contains all the necessary files:
- `app.py` (main Flask application)
- `requirements.txt` (Python dependencies)
- `vercel.json` (Vercel configuration)
- `templates/` folder (HTML templates)
- `.vercelignore` (deployment exclusions)

### 2. Deploy to Vercel
1. **Connect your GitHub repository** to Vercel
2. **Import the project** in Vercel dashboard
3. **Set environment variables**:
   - Go to Project Settings → Environment Variables
   - Add `GROQ_API_KEY` with your actual API key
4. **Deploy** - Vercel will automatically build and deploy your app

### 3. Configuration Files Explained

#### `vercel.json`
```json
{
  "version": 2,
  "builds": [
    {
      "src": "app.py",
      "use": "@vercel/python"
    }
  ],
  "routes": [
    {
      "src": "/(.*)",
      "dest": "app.py"
    }
  ]
}
```

#### `requirements.txt`
```
Flask==2.3.3
groq==0.4.2
python-dotenv==1.0.0
```

## 🎯 Key Features Implementation

### AI Chatbot System
```python
def chatbot_response(messages):
    if not client:
        return "I'm sorry, the chatbot service is currently unavailable."
    
    try:
        response = client.chat.completions.create(
            model="llama3-8b-8192",
            messages=[
                {"role": "system", "content": "You are an expert courier assistant..."},
                *messages
            ]
        )
        return response.choices[0].message.content
    except Exception as e:
        return "I'm sorry, I'm having trouble processing your request."
```

### Pricing Estimator
```python
def compute_price_estimate(distance_km: float, weight_kg: float, service_speed: str) -> dict:
    base_fee = 5.00
    per_km = 0.75
    per_kg = 0.60
    speed_multiplier_map = {
        "standard": 1.0,
        "express": 1.35,
        "same_day": 1.85,
    }
    # ... calculation logic
```

### Interactive Frontend
- **Auto-opening chatbot** with sound effects
- **Scroll-triggered animations** for service cards and gallery
- **Real-time pricing calculator** with instant results
- **Responsive navigation** with smooth transitions

## 📁 Project Structure

```
chatbot/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── vercel.json           # Vercel deployment config
├── runtime.txt           # Python version specification
├── .vercelignore         # Files to exclude from deployment
├── .env                  # Environment variables (not in repo)
├── .gitignore           # Git ignore rules
├── README.md            # This file
└── templates/           # HTML templates
    ├── index.html       # Home page
    ├── services.html    # Services page
    ├── pricing.html     # Pricing page with estimator
    └── contact.html     # Contact page
```

## 🔧 Customization

### Changing the AI Model
In `app.py`, modify the model parameter:
```python
response = client.chat.completions.create(
    model="llama3-8b-8192",  # Change to your preferred model
    # ...
)
```

### Updating Pricing
Modify the pricing parameters in `compute_price_estimate()`:
```python
base_fee = 5.00      # Base delivery fee
per_km = 0.75        # Cost per kilometer
per_kg = 0.60        # Cost per kilogram
```

### Customizing the UI
- **Colors**: Update CSS variables in the template files
- **Images**: Replace URLs in the gallery sections
- **Content**: Modify text content in HTML templates

## 🐛 Troubleshooting

### Common Issues

1. **Chatbot not responding**
   - Check if `GROQ_API_KEY` is set correctly
   - Verify your Groq API key is valid and has credits

2. **Deployment fails on Vercel**
   - Ensure all files are committed to your repository
   - Check that `requirements.txt` is in the root directory
   - Verify `vercel.json` configuration is correct

3. **Pricing estimator not working**
   - Check browser console for JavaScript errors
   - Verify the `/estimate` endpoint is accessible

### Environment Variables
Make sure these are set in your Vercel dashboard:
- `GROQ_API_KEY`: Your Groq API key

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

## 🙏 Acknowledgments

- **Groq AI** for providing the LLM API
- **Vercel** for the deployment platform
- **Unsplash** for the beautiful courier images
- **Flaticon** for the service icons

## 📞 Support

If you encounter any issues or have questions:
1. Check the troubleshooting section above
2. Review the Vercel deployment logs
3. Open an issue in the repository

---

**Built with ❤️ for modern courier services**
