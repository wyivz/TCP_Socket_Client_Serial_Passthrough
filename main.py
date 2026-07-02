import socket
import threading
import sys
import time
import traceback

def receive_thread(client_socket):
    """
    独立的工作线程：专门用于死循环接收来自串口(TCP Server)的数据
    """
    while True:
        try:
            # 阻塞等待接收数据，最大接收 1024 字节
            response = client_socket.recv(1024)
            if not response:
                print("\n[系统] 模块已主动断开连接。")
                break
            
            # 打印收到的数据 (忽略无法解码的非ASCII字符)
            data_str = response.decode('ascii', errors='ignore').strip()
            if data_str:
                print(f"\n[串口接收] <- {data_str}")
                print("[请输入 AT 指令(已自动添加\"\\r\\n\"换行)] -> ", end="", flush=True) # 恢复输入提示
                
        except socket.timeout:
            # 如果设置了超时，忽略超时继续循环
            continue
        except Exception as e:
            print(f"\n[系统] 接收线程退出: {e}")
            break

def main_logic():
    """
    主业务逻辑
    """
    # 1. 将输入移入逻辑内，防止用户输入非数字端口时直接闪退
    try:
        MODULE_IP = input("请输入串口透传模块的IP：").strip()
        port_input = input("请输入串口透传服务端口：").strip()
        MODULE_PORT = int(port_input)
    except ValueError:
        print("\n[错误] 端口号必须是纯数字！输入有误，程序即将停止。")
        return # 优雅返回，触发外层的防闪退

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # 取消超时设置，让 recv 可以一直阻塞等待新数据
    client.settimeout(None) 
    
    try:
        print(f"[系统] 正在连接 {MODULE_IP}:{MODULE_PORT} ...")
        client.connect((MODULE_IP, MODULE_PORT))
        print("[系统] -> 连接成功！您可以开始输入指令了。")
        print("[提示] 输入 'exit' 可正常退出；按 Ctrl + C 可强制中断。\n")
        
        # 启动独立的接收线程
        recv_thread = threading.Thread(target=receive_thread, args=(client,))
        recv_thread.daemon = True # 设置为守护线程，主程序退出时自动销毁
        recv_thread.start()
        
        # 主线程：专门负责读取键盘输入并发送给模块
        while True:
            cmd = input("[请输入 AT 指令(已自动添加\"\\r\\n\"换行)] -> ")
            if cmd.lower() == 'exit':
                print("[系统] 正在退出...")
                break
                
            # 发送指令，务必加上回车换行 \r\n
            if cmd:
                full_cmd = f"{cmd}\r\n"
                client.sendall(full_cmd.encode('ascii'))
                # 发送后稍微等待一下，避免打印混淆
                time.sleep(0.1) 
                
    except ConnectionRefusedError:
        print("\n[错误] 连接被拒绝。请检查模块 IP、端口是否正确，以及透传服务是否已启动。")
    except Exception as e:
        print(f"\n[错误] 通信异常: {e}")
    finally:
        client.close()
        # 注意：这里去掉了原有的 sys.exit(0)，让函数正常结束，从而走到外层的 finally 防闪退逻辑

if __name__ == "__main__":
    try:
        # 运行核心逻辑
        main_logic()
        
    except KeyboardInterrupt:
        # 捕获用户在任意时刻按下的 Ctrl + C
        print("\n用户手动 [Ctrl + C] 中断信号")
        
    except Exception as e:
        # 捕获其他未知的系统级崩溃
        print("\n程序发生异常,已崩溃：")
        traceback.print_exc()
        
    finally:
        # 终极防闪退锁：无论正常退出、报错还是 Ctrl+C，都会执行这里
        print("\n" + "="*50)
        print("程序已停止运行。")
        print("手动关闭，或按下 [Enter] 键退出。")
        print("="*50)
        
        # 用 input() 死死卡住 CLI 窗口
        input()