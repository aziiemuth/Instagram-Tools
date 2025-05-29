import os
import json
import chardet

def deteksi_encoding(file_path):
    with open(file_path, 'rb') as f:
        result = chardet.detect(f.read())
        return result['encoding']

# Folder tempat file JSON berada
folder_json = "./data"

# Daftar file dan deskripsi sesuai permintaan
file_deskripsi = {
    "blocked_profiles.json": "Daftar akun yang kamu blokir.",
    "close_friends.json": "Daftar akun yang masuk ke daftar teman dekat (untuk story).",
    "follow_requests_you've_received.json": "Daftar permintaan follow yang masuk ke akunmu (jika akunmu privat).",
    "hide_story_from.json": "Daftar akun yang kamu sembunyikan story-nya, artinya mereka tidak bisa melihat story kamu.",
    "pending_follow_requests.json": "Daftar permintaan follow yang belum diterima oleh pengguna lain (kamu yang mengirim permintaan, tapi belum di-accept).",
    "profiles_you've_favorited.json": "Daftar akun yang kamu favoritkan (fitur baru di Instagram, biasanya prioritas tampilannya lebih tinggi di feed).",
    "recent_follow_requests.json": "Daftar akun yang baru-baru ini kamu minta untuk follow.",
    "recently_unfollowed_profiles.json": "Daftar akun yang baru saja kamu unfollow.",
    "removed_suggestions.json": "Daftar akun dari saran follow yang kamu hapus atau tolak.",
    "restricted_profiles.json": "Daftar akun yang kamu batasi (restricted: bisa lihat akunmu tapi komentarnya tersembunyi, dll)."
}

# Mapping file ke key JSON utama
file_keys = {
    "blocked_profiles.json": "relationships_blocked_users",
    "close_friends.json": "relationships_close_friends",
    "follow_requests_you've_received.json": "relationships_follow_requests_received",
    "hide_story_from.json": "relationships_hide_stories_from",
    "pending_follow_requests.json": "relationships_follow_requests_sent",
    "profiles_you've_favorited.json": "relationships_feed_favorites",
    "recent_follow_requests.json": "relationships_permanent_follow_requests",
    "recently_unfollowed_profiles.json": "relationships_unfollowed_users",
    "removed_suggestions.json": "relationships_dismissed_suggested_users",
    "restricted_profiles.json": "relationships_restricted_users"
}

followers_set = set()
following_set = set()

for file_name, judul in file_deskripsi.items():
    file_path = os.path.join(folder_json, file_name)
    if not os.path.exists(file_path):
        continue

    encoding = deteksi_encoding(file_path)
    with open(file_path, "r", encoding=encoding) as file:
        data = json.load(file)

    key = file_keys[file_name]
    akun_list = []
    for entry in data.get(key, []):
        if entry.get("string_list_data"):
            info = entry["string_list_data"][0]
            username = info.get("value")
            if not username:
                href = info.get("href", "")
                if href.startswith("https://www.instagram.com/"):
                    username = href.strip("/").split("/")[-1]
            if username:
                akun_list.append(username)

    print(f"\n{judul}")
    for akun in akun_list:
        print(f"- {akun}")

# Cari akun yang unfollow kita (kita follow dia, tapi dia tidak follow balik)
followers_file = os.path.join(folder_json, "followers_1.json")
following_file = os.path.join(folder_json, "following.json")

if os.path.exists(followers_file):
    encoding = deteksi_encoding(followers_file)
    with open(followers_file, "r", encoding=encoding) as f:
        followers_data = json.load(f)
        followers_set = {entry["string_list_data"][0].get("value") for entry in followers_data if entry.get("string_list_data")}

if os.path.exists(following_file):
    encoding = deteksi_encoding(following_file)
    with open(following_file, "r", encoding=encoding) as f:
        following_data = json.load(f)
        following_set = {entry["string_list_data"][0].get("value") for entry in following_data.get("relationships_following", []) if entry.get("string_list_data")}

unfollowers = following_set - followers_set

print("\n==============================")
if unfollowers:
    print("Daftar akun yang tidak follow balik kamu:")
    for akun in sorted(unfollowers):
        print(f"- {akun}")
else:
    print("Semua akun yang kamu follow juga mem-follow kamu balik.")
print("==============================")
