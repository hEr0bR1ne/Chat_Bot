#!/usr/bin/env python3
"""
音频设备选择工具
用于查看可用的音频设备并测试录音和播放功能
"""

from core.audio import AudioProcessor
import time

class DeviceSelector:
    def __init__(self):
        self.audio = AudioProcessor()
        
    def show_devices(self):
        """显示所有可用设备"""
        print("\n" + "="*50)
        print("音频设备选择工具")
        print("="*50)
        
        input_devices, output_devices = self.audio.list_audio_devices()
        
        print("\n📱 可用录音设备:")
        for device in input_devices:
            print(f"  {device['index']}: {device['name']}")
            
        print("\n🔊 可用播放设备:")
        for device in output_devices:
            print(f"  {device['index']}: {device['name']}")
            
        return input_devices, output_devices
    
    def test_recording(self, device_index):
        """测试录音设备"""
        print(f"\n🎤 测试录音设备 {device_index}...")
        
        # 设置录音设备
        if not self.audio.set_input_device(device_index):
            return False
            
        print("开始录音 (3秒)...")
        
        # 录音测试
        recording_done = False
        def on_record_complete(success, filename=None, error=None):
            nonlocal recording_done
            recording_done = True
            if success:
                print(f"✅ 录音成功，文件: {filename}")
            else:
                print(f"❌ 录音失败: {error}")
        
        self.audio.record_audio("test_recording.wav", on_record_complete)
        
        # 等待录音完成
        while not recording_done:
            time.sleep(0.1)
            
        return recording_done
    
    def test_playback(self, device_index):
        """测试播放设备"""
        print(f"\n🔊 测试播放设备 {device_index}...")
        
        # 设置播放设备
        if not self.audio.set_output_device(device_index):
            return False
            
        print("播放测试音频...")
        
        # 播放测试
        playback_done = False
        def on_play_complete(success, error=None):
            nonlocal playback_done
            playback_done = True
            if success:
                print("✅ 播放成功")
            else:
                print(f"❌ 播放失败: {error}")
        
        # 如果有测试录音文件，播放它；否则尝试播放系统文件
        try:
            self.audio.play_audio("test_recording.wav", on_play_complete)
            
            # 等待播放完成
            start_time = time.time()
            while not playback_done and (time.time() - start_time) < 10:
                time.sleep(0.1)
                
        except Exception as e:
            print(f"❌ 播放测试失败: {e}")
            return False
            
        return playback_done
    
    def interactive_selection(self):
        """交互式设备选择"""
        input_devices, output_devices = self.show_devices()
        
        if not input_devices and not output_devices:
            print("❌ 没有找到可用的音频设备")
            return None, None
        
        selected_input = None
        selected_output = None
        
        # 选择录音设备
        if input_devices:
            while True:
                try:
                    choice = input(f"\n请选择录音设备 (0-{len(input_devices)-1}, 或 'skip' 跳过): ")
                    if choice.lower() == 'skip':
                        break
                    
                    device_idx = int(choice)
                    if 0 <= device_idx < len(input_devices):
                        actual_index = input_devices[device_idx]['index']
                        if self.test_recording(actual_index):
                            selected_input = actual_index
                            break
                    else:
                        print("❌ 无效选择，请重试")
                except ValueError:
                    print("❌ 请输入有效数字")
                except KeyboardInterrupt:
                    print("\n\n👋 已取消选择")
                    return None, None
        
        # 选择播放设备  
        if output_devices:
            while True:
                try:
                    choice = input(f"\n请选择播放设备 (0-{len(output_devices)-1}, 或 'skip' 跳过): ")
                    if choice.lower() == 'skip':
                        break
                        
                    device_idx = int(choice)
                    if 0 <= device_idx < len(output_devices):
                        actual_index = output_devices[device_idx]['index']
                        if self.test_playback(actual_index):
                            selected_output = actual_index
                            break
                    else:
                        print("❌ 无效选择，请重试")
                except ValueError:
                    print("❌ 请输入有效数字")
                except KeyboardInterrupt:
                    print("\n\n👋 已取消选择")
                    return None, None
        
        # 显示最终选择
        print("\n" + "="*50)
        print("设备选择结果:")
        if selected_input is not None:
            input_name = next(d['name'] for d in input_devices if d['index'] == selected_input)
            print(f"🎤 录音设备: {selected_input} - {input_name}")
        else:
            print("🎤 录音设备: 使用系统默认")
            
        if selected_output is not None:
            output_name = next(d['name'] for d in output_devices if d['index'] == selected_output)
            print(f"🔊 播放设备: {selected_output} - {output_name}")
        else:
            print("🔊 播放设备: 使用系统默认")
        
        print("="*50)
        
        return selected_input, selected_output

def main():
    """主函数"""
    selector = DeviceSelector()
    
    try:
        # 交互式选择设备
        input_device, output_device = selector.interactive_selection()
        
        if input_device is not None or output_device is not None:
            print(f"\n💾 建议在程序中使用以下配置:")
            print(f"AudioProcessor(input_device_index={input_device}, output_device_index={output_device})")
        
    except Exception as e:
        print(f"❌ 程序出错: {e}")
    finally:
        # 清理资源
        del selector.audio

if __name__ == "__main__":
    main() 