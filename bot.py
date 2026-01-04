import telebot
from telebot import types
import yt_dlp
import os
import time
from keep_alive import keep_alive

# 🔹 আপনার বট টোকেন দিন
API_TOKEN = '8477494191:AAGz9TeMc7msC-KLdCu10ZOglNVZXk_t1ZM'
bot = telebot.TeleBot(API_TOKEN)

# ==========================================
# 💾 স্মার্ট মেমোরি সিস্টেম (ডাটাবেস)
# ==========================================
# এই সিস্টেমটি মনে রাখবে কে কে রুলস এক্সেপ্ট করেছে
USER_FILE = "verified_users.txt"

def load_verified_users():
    if not os.path.exists(USER_FILE):
        return set()
    with open(USER_FILE, "r") as f:
        return set(line.strip() for line in f)

def save_verified_user(chat_id):
    with open(USER_FILE, "a") as f:
        f.write(f"{chat_id}\n")
    verified_users.add(str(chat_id))

# বট চালু হওয়ার সময় মেমোরি লোড করবে
verified_users = load_verified_users()

# ==========================================
# 1. স্টার্ট এবং পার্মানেন্ট এগ্রিমেন্ট চেক
# ==========================================
@bot.message_handler(commands=['start'])
def send_welcome(message):
    chat_id = str(message.chat.id)
    user_name = message.from_user.first_name

    # ইউজার কি আগে সম্মতি দিয়েছে? চেক করা হচ্ছে...
    if chat_id in verified_users:
        show_main_menu(message.chat.id, user_name)
    else:
        # সম্মতি না দিলে রুলস দেখাবে (একবারই)
        markup = types.InlineKeyboardMarkup()
        btn_agree = types.InlineKeyboardButton("✅ আমি সম্মত", callback_data="agree_terms")
        markup.add(btn_agree)

        rules_text = (
            f"👋 **স্বাগতম! {user_name}**\n\n"
            "এই বটটি ব্যবহার করে আপনি সহজেই TikTok ভিডিও ডাউনলোড করতে পারবেন—দ্রুত, সহজ ও সম্পূর্ণ ফ্রি 📥\n\n"
            "📜 **ব্যবহার নীতিমালা:**\n"
            "• বটটি শুধুমাত্র ব্যক্তিগত ও বৈধ ব্যবহারের জন্য\n"
            "• ডাউনলোড করা কনটেন্টের কপিরাইট দায়ভার ব্যবহারকারীর\n"
            "• স্প্যাম বা অপব্যবহার করলে অ্যাক্সেস বন্ধ করা হতে পারে\n"
            "• নিয়ম পরিবর্তনের অধিকার ডেভেলপারের সংরক্ষিত\n\n"
            "বট ব্যবহার করে আপনি উপরোক্ত শর্তে সম্মত হচ্ছেন ✅\n\n"
            "🛠 **Developer:** Ayman Hasan Shaan\n"
            "🏷 **Brand:** Swygen IT"
        )
        bot.send_message(message.chat.id, rules_text, reply_markup=markup, parse_mode="Markdown")

# 'আমি সম্মত' বাটন হ্যান্ডলার
@bot.callback_query_handler(func=lambda call: call.data == "agree_terms")
def handle_agreement(call):
    chat_id = call.message.chat.id
    user_name = call.from_user.first_name
    
    # মেমোরিতে সেভ করা হচ্ছে
    save_verified_user(chat_id)
    
    # আগের মেসেজ ডিলিট করে ক্লিন লুক দেওয়া
    try:
        bot.delete_message(chat_id, call.message.message_id)
    except:
        pass
        
    bot.answer_callback_query(call.id, "ধন্যবাদ! যাচাইকরণ সফল হয়েছে।")
    
    # স্বাগতম মেসেজ এবং মেনু
    welcome_msg = f"✅ **অভিনন্দন! {user_name}**\nআপনার অ্যাকাউন্ট ভেরিফাইড হয়েছে। এখন আপনি আনলিমিটেড ডাউনলোড করতে পারবেন।"
    bot.send_message(chat_id, welcome_msg, parse_mode="Markdown")
    show_main_menu(chat_id, user_name)

# ==========================================
# 2. মেইন ড্যাশবোর্ড (Professional UI)
# ==========================================
def show_main_menu(chat_id, user_name):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    btn_download = types.KeyboardButton("⬇️ ভিডিও ডাউনলোড")
    btn_dev = types.KeyboardButton("👨‍💻 ডেভেলপার ইনফো")
    btn_policy = types.KeyboardButton("📜 নীতিমালা")
    markup.add(btn_download, btn_dev, btn_policy)

    bot.send_message(chat_id, "👇 **নিচের মেনু থেকে অপশন নির্বাচন করুন:**", reply_markup=markup, parse_mode="Markdown")

# ==========================================
# 3. ডেভেলপার ইনফো (Swygen Branding)
# ==========================================
@bot.message_handler(func=lambda message: message.text == "👨‍💻 ডেভেলপার ইনফো")
def dev_info(message):
    markup = types.InlineKeyboardMarkup()
    btn_site = types.InlineKeyboardButton("🌐 অফিসিয়াল ওয়েবসাইট", url="https://swygen.xyz")
    markup.add(btn_site)

    info_text = (
        "🛠 **ডেভেলপার তথ্য**\n\n"
        "👨‍💻 **ডেভেলপার:** Ayman Hasan Shaan\n"
        "🏷 **ব্র্যান্ড:** Swygen IT\n\n"
        "🚀 **Swygen IT** আধুনিক প্রযুক্তি ব্যবহার করে সহজ, দ্রুত ও নির্ভরযোগ্য ডিজিটাল সল্যুশন তৈরি করে। আমাদের লক্ষ্য হলো ব্যবহারকারীদের জন্য কার্যকর, নিরাপদ ও ব্যবহারবান্ধব সার্ভিস প্রদান করা।\n\n"
        "🌐 আমাদের সকল সার্ভিস, প্রজেক্ট ও আপডেট সম্পর্কে বিস্তারিত জানতে ভিজিট করুন আমাদের অফিসিয়াল ওয়েবসাইটে।\n\n"
        "💡 আপনার মতামত ও পরামর্শ আমাদের আরও ভালো করতে সাহায্য করে।\n\n"
        "**ধন্যবাদ আমাদের সাথে থাকার জন্য ❤️**"
    )
    bot.send_message(message.chat.id, info_text, reply_markup=markup, parse_mode="Markdown")

# ==========================================
# 4. নীতিমালা সেকশন
# ==========================================
@bot.message_handler(func=lambda message: message.text == "📜 নীতিমালা")
def policy_info(message):
    policy_text = (
        "👋 **স্বাগতম!**\n"
        "আমি **আয়মান হাসান শান** —\n"
        "আমি আপনাদের জন্য সম্পূর্ণ ফ্রি **TikTok Video Downloader Telegram Bot** তৈরি করেছি।\n\n"
        "🎯 **এই বটের মাধ্যমে আপনি যা করতে পারবেন:**\n"
        "✅ TikTok ভিডিও ওয়াটারমার্ক ছাড়া ডাউনলোড\n"
        "✅ HD কোয়ালিটিতে ভিডিও সেভ\n"
        "✅ কোনো লগইন বা পেমেন্ট ছাড়াই ১০০% ফ্রি\n"
        "✅ খুব সহজ ও দ্রুত ব্যবহারযোগ্য\n\n"
        "📌 **ব্যবহার করার নিয়ম:**\n"
        "1️⃣ TikTok ভিডিওর লিংক কপি করুন\n"
        "2️⃣ বটে পাঠান\n"
        "3️⃣ কয়েক সেকেন্ড অপেক্ষা করুন\n"
        "4️⃣ ভিডিও ডাউনলোড করুন 📥\n\n"
        "💡 **নোট:**\n"
        "এই বটটি শুধুমাত্র শিক্ষামূলক ও ব্যক্তিগত ব্যবহারের জন্য\n"
        "কোনো ভিডিওর কপিরাইট দায়ভার ব্যবহারকারীর নিজের\n\n"
        "❤️ যদি বটটি ভালো লাগে, বন্ধুদের সাথে শেয়ার করুন\n"
        "🐞 কোনো সমস্যা বা ফিডব্যাক থাকলে জানাতে ভুলবেন না\n\n"
        "ধন্যবাদ সবাইকে 🙏\n"
        "— **Developer: আয়মান হাসান শান**"
    )
    bot.send_message(message.chat.id, policy_text, parse_mode="Markdown")

# ==========================================
# 5. ভিডিও ডাউনলোড প্রসেস (Ultra HD Logic)
# ==========================================
user_links = {} # টেম্পোরারি লিংক স্টোরেজ

@bot.message_handler(func=lambda message: message.text == "⬇️ ভিডিও ডাউনলোড")
def ask_for_link(message):
    chat_id = str(message.chat.id)
    # ডাবল চেক: যদি ফাইল ডিলিট হয়ে যায়, আবার রুলস দেখাবে
    if chat_id not in verified_users:
        send_welcome(message)
        return
        
    msg = bot.send_message(message.chat.id, "🔗 দয়া করে আপনার **TikTok ভিডিওর লিংকটি** দিন:", parse_mode="Markdown")
    bot.register_next_step_handler(msg, process_link)

def process_link(message):
    url = message.text
    chat_id = message.chat.id

    if "tiktok.com" not in url:
        bot.send_message(chat_id, "❌ **ভুল লিংক!** দয়া করে একটি সঠিক TikTok লিংক দিন।", parse_mode="Markdown")
        return

    user_links[chat_id] = url

    # ফরম্যাট সিলেকশন বাটন
    markup = types.InlineKeyboardMarkup(row_width=1)
    btn_nowm = types.InlineKeyboardButton("🚫 Without Watermark", callback_data="type_nowm")
    btn_hd = types.InlineKeyboardButton("🌟 HD Quality (2K/4K)", callback_data="type_hd")
    btn_mp3 = types.InlineKeyboardButton("🎵 MP3 (Audio Only)", callback_data="type_mp3")
    markup.add(btn_nowm, btn_hd, btn_mp3)

    bot.send_message(chat_id, "📥 **আপনি কোন ফরম্যাটে ডাউনলোড করতে চান?**", reply_markup=markup, parse_mode="Markdown")

# ==========================================
# 6. ডাউনলোড ইঞ্জিন (2K/4K Support)
# ==========================================
@bot.callback_query_handler(func=lambda call: call.data in ["type_nowm", "type_hd", "type_mp3"])
def handle_download(call):
    chat_id = call.message.chat.id
    
    if chat_id not in user_links:
        bot.send_message(chat_id, "⚠️ **টাইমআউট!** আবার লিংক দিন।", parse_mode="Markdown")
        return

    url = user_links[chat_id]
    format_type = call.data
    
    # লোডিং মেসেজ
    processing_msg = bot.edit_message_text(chat_id=chat_id, message_id=call.message.message_id, text="⏳ **প্রসেসিং হচ্ছে...**\nSwygen সার্ভার থেকে সর্বোচ্চ কোয়ালিটি (2K/4K) খোঁজা হচ্ছে...", parse_mode="Markdown")

    try:
        # ইউনিক ফাইল নেম (যাতে মিক্স না হয়)
        file_name = f"Swygen_{chat_id}_{int(time.time())}"
        ydl_opts = {}

        # 🎯 অ্যাডভান্সড কোয়ালিটি লজিক
        if format_type == "type_mp3":
            file_name += ".mp3"
            ydl_opts = {
                'format': 'bestaudio/best',
                'outtmpl': file_name,
                'postprocessors': [{'key': 'FFmpegExtractAudio','preferredcodec': 'mp3',}],
            }
        elif format_type == "type_hd":
            file_name += ".mp4"
            # এখানে 'bestvideo+bestaudio' ব্যবহার করা হয়েছে যা 2K/4K ক্যাপচার করবে
            ydl_opts = {
                'format': 'bestvideo+bestaudio/best', 
                'outtmpl': file_name,
                'merge_output_format': 'mp4',
            }
        else: # Without Watermark (Standard)
            file_name += ".mp4"
            ydl_opts = {
                'format': 'best',
                'outtmpl': file_name,
            }

        # ডাউনলোড এক্সিকিউশন
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        # আপলোড অ্যাকশন
        bot.send_chat_action(chat_id, 'upload_video')

        # ফাইল সেন্ড
        with open(file_name, 'rb') as file:
            caption_text = (
                "✅ **ডাউনলোড সম্পন্ন!**\n"
                "────────────────\n"
                "🏷 **Brand:** Swygen IT\n"
                "🛠 **Dev:** Ayman Hasan Shaan"
            )
            
            if format_type == "type_mp3":
                bot.send_audio(chat_id, file, caption=caption_text, parse_mode="Markdown")
            else:
                bot.send_video(chat_id, file, caption=caption_text, parse_mode="Markdown")

        # 🔹 অটোমেটিক ফিডব্যাক মেসেজ
        markup = types.InlineKeyboardMarkup()
        btn_site = types.InlineKeyboardButton("🌐 Visit Swygen.xyz", url="https://swygen.xyz")
        markup.add(btn_site)
        
        user_name = call.from_user.first_name
        feedback_msg = (
            f"প্রিয় **{user_name}**, সার্ভিস টি কী রকম লাগলো জানাতে ভুলবেন না ❤️\n\n"
            "আমাদের ওয়েবসাইটে ভিজিট করতে নিচের বাটনে ক্লিক করুন 👇"
        )
        
        bot.send_message(chat_id, feedback_msg, reply_markup=markup, parse_mode="Markdown")
        bot.delete_message(chat_id, processing_msg.message_id) # প্রসেসিং মেসেজ ডিলিট

        # সার্ভার ক্লিনআপ
        if os.path.exists(file_name):
            os.remove(file_name)

    except Exception as e:
        error_msg = "❌ **ডাউনলোড ব্যর্থ হয়েছে!**\nভিডিওটি প্রাইভেট হতে পারে অথবা সার্ভার রেসপন্স করছে না।"
        bot.send_message(chat_id, error_msg, parse_mode="Markdown")
        if os.path.exists(file_name):
            try: os.remove(file_name)
            except: pass

# Keep Alive & Run
keep_alive()
bot.polling(none_stop=True)
