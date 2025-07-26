import speedtest as speedtest_module

def run_speedtest():
    st = speedtest_module.Speedtest()
    print("🧪 Testing download speed...")
    download = st.download() / 1_000_000
    print("🧪 Testing upload speed...")
    upload = st.upload() / 1_000_000
    ping = st.results.ping
    print(f"⬇️ Download: {download:.2f} Mbps")
    print(f"⬆️ Upload: {upload:.2f} Mbps")
    print(f"📡 Ping: {ping} ms")