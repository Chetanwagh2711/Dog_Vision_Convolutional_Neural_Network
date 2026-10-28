import os
import streamlit as st
import numpy as np
from PIL import Image

# ---------------------------------------------------------
# Page Configuration
# ---------------------------------------------------------
st.set_page_config(
    page_title="Dog Vision 🐶 - Kids Pup Detective!",
    page_icon="🐾",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ---------------------------------------------------------
# Compatibility Patch for Keras Version Differences
# ---------------------------------------------------------
def _apply_keras_compatibility_patches():
    """
    Prevents deserialization errors when a model saved in a newer Keras version
    (such as Google Colab) is loaded on a local environment containing unexpected kwargs
    like 'quantization_config'.
    """
    try:
        import keras
        orig_dense_init = keras.layers.Dense.__init__
        def patched_dense_init(self, *args, **kwargs):
            kwargs.pop("quantization_config", None)
            return orig_dense_init(self, *args, **kwargs)
        keras.layers.Dense.__init__ = patched_dense_init
    except Exception:
        pass

    try:
        import tensorflow as tf
        orig_tf_dense_init = tf.keras.layers.Dense.__init__
        def patched_tf_dense_init(self, *args, **kwargs):
            kwargs.pop("quantization_config", None)
            return orig_tf_dense_init(self, *args, **kwargs)
        tf.keras.layers.Dense.__init__ = patched_tf_dense_init
    except Exception:
        pass

_apply_keras_compatibility_patches()

# ---------------------------------------------------------
# Ultra-Fun Kids Cartoon Theme (Sun, Rainbow, Butterflies, Dogs)
# ---------------------------------------------------------
KIDS_CARTOON_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Fredoka:wght@400;600;700&family=Chewy&family=Quicksand:wght@600;700&display=swap');

/* Overall Kids Cartoon World */
.stApp {
    background: linear-gradient(180deg, #b3e5fc 0%, #e1f5fe 30%, #fff9c4 55%, #c8e6c9 75%, #81c784 100%) !important;
    font-family: 'Fredoka', 'Quicksand', sans-serif !important;
    overflow-x: hidden !important;
}

/* Big Smiling Cartoon Sun */
.cartoon-sun {
    position: fixed;
    top: 25px;
    right: 40px;
    width: 90px;
    height: 90px;
    background: radial-gradient(circle, #fff176 30%, #fbc02d 100%);
    border-radius: 50%;
    box-shadow: 0 0 35px #ffee58, 0 0 60px rgba(255, 238, 88, 0.6);
    z-index: 1;
    pointer-events: none;
    animation: sunPulse 3s ease-in-out infinite alternate;
}
.sun-face {
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    font-size: 48px;
    line-height: 1;
    user-select: none;
}
@keyframes sunPulse {
    0% { transform: scale(1) rotate(0deg); }
    100% { transform: scale(1.1) rotate(10deg); }
}

/* Floating Rainbow */
.cartoon-rainbow {
    position: fixed;
    top: 30px;
    left: 50px;
    font-size: 65px;
    z-index: 1;
    opacity: 0.85;
    animation: rainbowFloat 5s ease-in-out infinite alternate;
    pointer-events: none;
}
@keyframes rainbowFloat {
    0% { transform: translateY(0px) rotate(-3deg); }
    100% { transform: translateY(-12px) rotate(3deg); }
}

/* Fluffy Cartoon Clouds */
.cloud {
    position: fixed;
    background: #ffffff;
    border-radius: 50px;
    opacity: 0.9;
    z-index: 1;
    pointer-events: none;
    animation: floatCloud linear infinite;
    box-shadow: 0 8px 18px rgba(0,0,0,0.06);
}
.cloud::before, .cloud::after {
    content: '';
    position: absolute;
    background: #ffffff;
    border-radius: 50%;
}
.cloud-1 { width: 150px; height: 50px; top: 12%; animation-duration: 38s; }
.cloud-1::before { width: 65px; height: 65px; top: -32px; left: 22px; }
.cloud-1::after { width: 75px; height: 75px; top: -38px; right: 25px; }

.cloud-2 { width: 190px; height: 60px; top: 22%; animation-duration: 52s; animation-delay: -18s; }
.cloud-2::before { width: 80px; height: 80px; top: -40px; left: 30px; }
.cloud-2::after { width: 90px; height: 90px; top: -45px; right: 35px; }

@keyframes floatCloud {
    from { left: -220px; }
    to { left: 105vw; }
}

/* Fluttering Cartoon Butterflies */
.butterfly {
    position: fixed;
    font-size: 32px;
    z-index: 3;
    pointer-events: none;
    animation: butterflyFly 14s ease-in-out infinite;
}
.butterfly-1 { top: 40%; left: -50px; animation-delay: 0s; }
.butterfly-2 { top: 55%; left: -50px; animation-delay: 7s; }

@keyframes butterflyFly {
    0% { left: -50px; transform: translateY(0) rotate(15deg); }
    25% { transform: translateY(-40px) rotate(-10deg); }
    50% { transform: translateY(20px) rotate(20deg); }
    75% { transform: translateY(-30px) rotate(-15deg); }
    100% { left: 105vw; transform: translateY(0) rotate(10deg); }
}

/* Rolling Cartoon Grass Hills */
.grass-hills {
    position: fixed;
    bottom: 0;
    left: 0;
    width: 100vw;
    height: 150px;
    background: radial-gradient(ellipse at 50% 100%, #66bb6a 0%, #43a047 65%, #2e7d32 100%);
    border-radius: 50% 50% 0 0 / 30px 30px 0 0;
    z-index: 2;
    pointer-events: none;
    box-shadow: 0 -10px 25px rgba(46, 125, 50, 0.3);
}

.flower-row {
    position: fixed;
    bottom: 100px;
    left: 0;
    width: 100vw;
    display: flex;
    justify-content: space-around;
    font-size: 28px;
    z-index: 2;
    pointer-events: none;
    user-select: none;
    animation: flowerSway 3s ease-in-out infinite alternate;
}
@keyframes flowerSway {
    0% { transform: rotate(-4deg); }
    100% { transform: rotate(4deg); }
}

/* Kids Doghouse on the Meadow Corner */
.doghouse-corner {
    position: fixed;
    bottom: 45px;
    right: 35px;
    font-size: 60px;
    z-index: 4;
    filter: drop-shadow(0 6px 10px rgba(0,0,0,0.25));
    user-select: none;
    pointer-events: none;
    animation: doghouseWiggle 4s ease-in-out infinite;
}
@keyframes doghouseWiggle {
    0%, 90%, 100% { transform: rotate(0deg); }
    93% { transform: rotate(-5deg) scale(1.05); }
    96% { transform: rotate(5deg) scale(1.05); }
}

/* Animated Running Cartoon Doggies Track */
.dog-track {
    position: fixed;
    bottom: 25px;
    left: 0;
    width: 100vw;
    height: 85px;
    z-index: 3;
    pointer-events: none;
    overflow: hidden;
}

.running-doggy {
    position: absolute;
    bottom: 0;
    display: inline-block;
    filter: drop-shadow(0 4px 6px rgba(0,0,0,0.2));
    animation: doggyRun linear infinite, doggyHop 0.4s ease-in-out infinite alternate;
}

.dog-ball { font-size: 26px; animation-duration: 15s, 0.32s; animation-delay: 0.8s, 0s; }
.dog-shiba { font-size: 48px; animation-duration: 15s, 0.38s; animation-delay: 0s, 0s; }
.dog-golden { font-size: 54px; animation-duration: 20s, 0.45s; animation-delay: -5s, 0.1s; }
.dog-bone { font-size: 30px; animation-duration: 20s, 0.3s; animation-delay: -4.3s, 0s; }
.dog-poodle { font-size: 46px; animation-duration: 17s, 0.35s; animation-delay: -10s, 0.15s; }
.dog-dalmatian { font-size: 50px; animation-duration: 22s, 0.42s; animation-delay: -15s, 0.05s; }
.dog-frisbee { font-size: 28px; animation-duration: 22s, 0.3s; animation-delay: -14.2s, 0s; }

@keyframes doggyRun {
    0% { left: -120px; transform: scaleX(1); }
    49% { left: 102vw; transform: scaleX(1); }
    50% { left: 102vw; transform: scaleX(-1); }
    99% { left: -120px; transform: scaleX(-1); }
    100% { left: -120px; transform: scaleX(1); }
}

@keyframes doggyHop {
    0% { transform: translateY(0px) rotate(0deg); }
    50% { transform: translateY(-16px) rotate(-8deg); }
    100% { transform: translateY(-4px) rotate(6deg); }
}

/* Kids Cartoon Hero Card */
.kids-hero-card {
    background: #ffffff;
    border: 5px solid #ffb300;
    border-radius: 35px;
    padding: 24px 30px;
    text-align: center;
    box-shadow: 0 14px 30px rgba(255, 179, 0, 0.25), 0 6px 0px #ff8f00;
    margin-bottom: 25px;
    position: relative;
    z-index: 10;
}

.kids-title {
    font-family: 'Chewy', 'Fredoka', cursive !important;
    font-size: 52px !important;
    color: #ff6f00 !important;
    letter-spacing: 1.5px;
    margin: 0 !important;
    text-shadow: 3px 3px 0px #ffe082;
}

.kids-tagline {
    font-family: 'Fredoka', sans-serif !important;
    font-size: 22px !important;
    font-weight: 600 !important;
    color: #2e7d32 !important;
    margin-top: 6px !important;
}

/* Kids Cartoon Content Box */
.kids-box {
    background: rgba(255, 255, 255, 0.95);
    border: 4px solid #81c784;
    border-radius: 30px;
    padding: 22px 26px;
    box-shadow: 0 10px 24px rgba(0, 0, 0, 0.08), 0 5px 0px #4caf50;
    margin-bottom: 20px;
    position: relative;
    z-index: 10;
}

/* Kids Upload Area Styling */
[data-testid="stFileUploader"] {
    background: #fffde7 !important;
    border: 4px dashed #ffb300 !important;
    border-radius: 25px !important;
    padding: 20px !important;
}

/* Winner Winner Doggy Dinner Badge */
.winner-badge {
    background: linear-gradient(135deg, #ff7043 0%, #f4511e 100%);
    border: 4px solid #ffcc80;
    color: #ffffff;
    border-radius: 28px;
    padding: 20px;
    text-align: center;
    box-shadow: 0 10px 25px rgba(244, 81, 30, 0.35), 0 5px 0px #d84315;
    margin-bottom: 20px;
    animation: bounceBadge 0.6s ease-out;
}
@keyframes bounceBadge {
    0% { transform: scale(0.85); opacity: 0; }
    60% { transform: scale(1.05); }
    100% { transform: scale(1); opacity: 1; }
}

.winner-crown { font-size: 38px; margin-bottom: 2px; }
.winner-breed {
    font-family: 'Chewy', 'Fredoka', cursive;
    font-size: 38px;
    margin: 4px 0;
    color: #ffffff;
    letter-spacing: 1px;
    text-shadow: 2px 2px 0px #bf360c;
}
.winner-stars { font-size: 20px; color: #fff59d; }

/* Cartoon Pill Progress Bars */
.kid-pill-row {
    margin-bottom: 14px;
}
.kid-pill-label {
    display: flex;
    justify-content: space-between;
    font-size: 17px;
    font-weight: 700;
    color: #2e7d32;
    margin-bottom: 5px;
}
.kid-pill-track {
    background: #e8f5e9;
    border: 2px solid #a5d6a7;
    border-radius: 20px;
    height: 20px;
    overflow: hidden;
}
.kid-pill-fill {
    height: 100%;
    background: linear-gradient(90deg, #ffb300 0%, #4caf50 100%);
    border-radius: 20px;
    transition: width 0.8s ease-in-out;
}

/* Fun Fact Card for Kids */
.fun-fact-card {
    background: #e1f5fe;
    border: 3px solid #4fc3f7;
    border-radius: 22px;
    padding: 14px 18px;
    margin-top: 15px;
    color: #0277bd;
    font-weight: 600;
    font-size: 15px;
    box-shadow: 0 4px 0px #29b6f6;
}
</style>

<!-- Background Cartoon Layer: Sun, Rainbow, Clouds, Butterflies, Flowers, Grass, Puppies -->
<div class="cartoon-sun"><div class="sun-face">☀️</div></div>
<div class="cartoon-rainbow">🌈</div>
<div class="cloud cloud-1"></div>
<div class="cloud cloud-2"></div>
<div class="butterfly butterfly-1">🦋</div>
<div class="butterfly butterfly-2">🦋</div>

<div class="flower-row">
    <span>🌸</span><span>🌼</span><span>🍄</span><span>🌻</span><span>🌷</span><span>🌼</span><span>🌸</span><span>🍄</span><span>🌻</span>
</div>

<div class="doghouse-corner">🏡🐶</div>
<div class="grass-hills"></div>

<div class="dog-track">
    <span class="running-doggy dog-ball">🎾</span>
    <span class="running-doggy dog-shiba">🐕</span>
    <span class="running-doggy dog-golden">🦮</span>
    <span class="running-doggy dog-bone">🦴</span>
    <span class="running-doggy dog-poodle">🐩</span>
    <span class="running-doggy dog-dalmatian">🐕‍🦺</span>
    <span class="running-doggy dog-frisbee">🥏</span>
</div>
"""

st.markdown(KIDS_CARTOON_CSS, unsafe_allow_html=True)

# ---------------------------------------------------------
# 120 Dog Breeds (Kaggle Dataset Alphabetical Order)
# ---------------------------------------------------------
DOG_BREEDS = [
    "affenpinscher", "afghan_hound", "african_hunting_dog", "airedale",
    "american_staffordshire_terrier", "appenzeller", "australian_terrier",
    "basenji", "basset", "beagle", "bedlington_terrier", "bernese_mountain_dog",
    "black-and-tan_coonhound", "blenheim_spaniel", "bloodhound", "bluetick",
    "border_collie", "border_terrier", "borzoi", "boston_bull",
    "bouvier_des_flandres", "boxer", "brabancon_griffon", "briard",
    "brittany_spaniel", "bull_mastiff", "cairn", "cardigan",
    "chesapeake_bay_retriever", "chihuahua", "chow", "clumber",
    "cocker_spaniel", "collie", "curly-coated_retriever", "dandie_dinmont",
    "dhole", "dingo", "doberman", "english_foxhound", "english_setter",
    "english_springer", "entlebucher", "eskimo_dog", "flat-coated_retriever",
    "french_bulldog", "german_shepherd", "german_short-haired_pointer",
    "giant_schnauzer", "golden_retriever", "gordon_setter", "great_dane",
    "great_pyrenees", "greater_swiss_mountain_dog", "groenendael",
    "ibizan_hound", "irish_setter", "irish_terrier", "irish_water_spaniel",
    "irish_wolfhound", "italian_greyhound", "japanese_spaniel", "keeshond",
    "kelpie", "kerry_blue_terrier", "komondor", "kuvasz", "labrador_retriever",
    "lakeland_terrier", "leonberg", "lhasa", "malamute", "malinois",
    "maltese_dog", "mexican_hairless", "miniature_pinscher", "miniature_poodle",
    "miniature_schnauzer", "newfoundland", "norfolk_terrier", "norwegian_elkhound",
    "norwich_terrier", "old_english_sheepdog", "otterhound", "papillon",
    "pekinese", "pembroke", "pomeranian", "pug", "redbone",
    "rhodesian_ridgeback", "rottweiler", "saint_bernard", "saluki", "samoyed",
    "schipperke", "scotch_terrier", "scottish_deerhound", "sealyham_terrier",
    "shetland_sheepdog", "shih-tzu", "siberian_husky", "silky_terrier",
    "soft-coated_wheaten_terrier", "staffordshire_bullterrier", "standard_poodle",
    "standard_schnauzer", "sussex_spaniel", "tibetan_mastiff", "tibetan_terrier",
    "toy_poodle", "toy_terrier", "vizsla", "walker_hound", "weimaraner",
    "welsh_springer_spaniel", "west_highland_white_terrier", "whippet",
    "wire-haired_fox_terrier", "yorkshire_terrier"
]

def format_breed_name(raw_name: str) -> str:
    """Format snake_case breed names into clean title case."""
    return raw_name.replace("_", " ").replace("-", " ").title()

# ---------------------------------------------------------
# Model Loading (Cached & Safe)
# ---------------------------------------------------------
@st.cache_resource(show_spinner="🦴 Waking up the Pup Detective...")
def load_classifier_model():
    """Locate and load .keras or .h5 model file with compile=False."""
    candidate_paths = [
        "mobilenetv2-full-data_DogVision.keras",
        "DogVision.h5",
        "DogVision.keras",
        "model.keras",
        "models/mobilenetv2-full-data_DogVision.keras",
        "models/DogVision.h5",
        "models/DogVision.keras"
    ]
    model_path = None
    for path in candidate_paths:
        if os.path.exists(path):
            model_path = path
            break

    if model_path is None:
        return None, "Puppy model not found! Place 'mobilenetv2-full-data_DogVision.keras' or 'DogVision.h5' in your project folder."

    # Try loading with compile=False (inference only)
    try:
        import tensorflow as tf
        model = tf.keras.models.load_model(model_path, compile=False)
        return model, model_path
    except Exception as tf_err:
        try:
            import keras
            model = keras.models.load_model(model_path, compile=False)
            return model, model_path
        except Exception as keras_err:
            return None, f"Error waking up model: {str(tf_err)}"

# ---------------------------------------------------------
# Image Preprocessing (Matches Google Colab Pipeline)
# ---------------------------------------------------------
IMG_SIZE = 224

def preprocess_image(pil_img: Image.Image) -> np.ndarray:
    """Preprocess PIL image: RGB, resize 224x224, float32 [0, 1]."""
    image = pil_img.convert("RGB")
    image = image.resize((IMG_SIZE, IMG_SIZE))
    img_array = np.array(image, dtype=np.float32) / 255.0
    return np.expand_dims(img_array, axis=0)

# ---------------------------------------------------------
# Main Kid-Friendly UI
# ---------------------------------------------------------
def main():
    # Big Cheerful Kids Title Card
    st.markdown(
        """
        <div class="kids-hero-card">
            <h1 class="kids-title">🐶 Dog Vision 🐾</h1>
            <p class="kids-tagline">Identify any dog breed instantly with deep learning across 120 breeds.</p>
        </div>
        """,
        unsafe_allow_html=True
    )

    # Load Model
    model, status_msg = load_classifier_model()
    if model is None:
        st.markdown(
            f"""
            <div class="kids-box" style="border-color: #ef5350; background: #ffebee;">
                <h3 style="color: #c62828; margin: 0;">🦴 Oops! Where is the Puppy Model?</h3>
                <p style="color: #b71c1c; margin-top: 8px;">{status_msg}</p>
            </div>
            """,
            unsafe_allow_html=True
        )
        st.stop()

    # Upload Section
    st.markdown(
        """
        <div class="kids-box">
            <h2 style="color: #ff6f00; margin-top: 0; font-family: 'Chewy', cursive; font-size: 32px;">
                📸 Show Me Your Doggy!
            </h2>
            <p style="color: #555; font-size: 16px; margin-bottom: 12px;">
                Pick a cute picture of a dog from your computer, or snap one with your camera!
            </p>
        """,
        unsafe_allow_html=True
    )

    tab_upload, tab_camera = st.tabs(["📁 Upload a Dog Photo", "📷 Snap with Camera"])
    uploaded_file = None

    with tab_upload:
        file_input = st.file_uploader(
            "Drop your doggy photo right here!",
            type=["jpg", "jpeg", "png", "bmp", "webp"],
            help="Choose a clear picture of any dog!"
        )
        if file_input:
            uploaded_file = file_input

    with tab_camera:
        camera_input = st.camera_input("Say Cheese, Puppy! 📸")
        if camera_input:
            uploaded_file = camera_input

    st.markdown('</div>', unsafe_allow_html=True)

    # Results & Fun Detection
    if uploaded_file is not None:
        try:
            image = Image.open(uploaded_file)
        except Exception as e:
            st.error(f"Cannot read image: {e}")
            st.stop()

        # Fun Kids Balloons Celebration!
        st.balloons()

        col_left, col_right = st.columns([1, 1], gap="large")

        with col_left:
            st.markdown(
                """
                <div class="kids-box" style="text-align: center;">
                    <h3 style="color: #2e7d32; font-family: 'Chewy', cursive; font-size: 30px; margin-top: 0;">
                        🐶 Your Cute Puppy!
                    </h3>
                """,
                unsafe_allow_html=True
            )
            st.image(image, use_container_width=True)
            st.markdown(
                """
                <p style="color: #7cb342; font-weight: 700; margin-top: 8px; font-size: 16px;">
                    ✨ Such a good doggy! ✨
                </p>
                </div>
                """,
                unsafe_allow_html=True
            )

        with col_right:
            st.markdown(
                """
                <div class="kids-box">
                    <h3 style="color: #ff6f00; font-family: 'Chewy', cursive; font-size: 32px; margin-top: 0;">
                        🎉 Detective Pup Found a Match!
                    </h3>
                """,
                unsafe_allow_html=True
            )

            with st.spinner("🐾 Sniffing the nose, wagging the tail..."):
                processed_tensor = preprocess_image(image)
                predictions = model.predict(processed_tensor, verbose=0)[0]

                top_5_indices = predictions.argsort()[-5:][::-1]
                top_5_breeds = [format_breed_name(DOG_BREEDS[i]) for i in top_5_indices]
                top_5_scores = [float(predictions[i]) * 100 for i in top_5_indices]

                best_breed = top_5_breeds[0]
                best_score = top_5_scores[0]

            # Winner Badge
            st.markdown(
                f"""
                <div class="winner-badge">
                    <div class="winner-crown">👑 🐾</div>
                    <div class="winner-stars">★ ★ ★ TOP BREED ★ ★ ★</div>
                    <h2 class="winner-breed">{best_breed}</h2>
                    <div style="font-size: 20px; font-weight: 700; margin-top: 4px;">
                        Confidence: {best_score:.1f}% Match!
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )

            # Top 5 Likely Breeds
            st.markdown('<h4 style="color: #2e7d32; margin-top: 15px; margin-bottom: 12px; font-size: 20px;">🦴 Top 5 Likely Breeds:</h4>', unsafe_allow_html=True)
            for breed, score in zip(top_5_breeds, top_5_scores):
                st.markdown(
                    f"""
                    <div class="kid-pill-row">
                        <div class="kid-pill-label">
                            <span>🐾 {breed}</span>
                            <span>{score:.1f}%</span>
                        </div>
                        <div class="kid-pill-track">
                            <div class="kid-pill-fill" style="width: {max(score, 4.0):.1f}%;"></div>
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

            # Puppy Fun Fact Box for Kids
            st.markdown(
                """
                <div class="fun-fact-card">
                    💡 <b>Pup Fun Fact:</b> Did you know a dog's sense of smell is up to 100,000 times more sensitive than a human's? That's why they can sniff out treats from miles away! 🦴
                </div>
                """,
                unsafe_allow_html=True
            )

            st.markdown('</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()