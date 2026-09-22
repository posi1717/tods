from SKBUK.skbuk_calibrator import SKBUKCalibrator

def test_calibrator():
    calibrator = SKBUKCalibrator()
    
    # ข้อมูลจำลองทดสอบ
    sample_data = {
        "content": "This is a public procurement notice complying with the Procurement Act 2023 regulations and PPN guidelines.",
        "source": "UK Cabinet Office"
    }
    
    result = calibrator.calibrate(sample_data)
    print("=== DIRECT CALIBRATION TEST RESULT ===")
    print(result)

if __name__ == "__main__":
    test_calibrator()
