## 无线OBD研发项目
#### 功能
- CANFD转WiFi；
- doip转wifi；8脚支持激活
- 通过WiFi控制DOIP、BCAN、PCAN的切换
- 支持12V充电电池功能

---

```mermaid
flowchart TD
    %% ----------------------------------------------------
    %% 样式定义
    %% ----------------------------------------------------
    classDef user fill:#fff3cd,stroke:#856404,stroke-width:1px;
    classDef router fill:#d4edda,stroke:#28a745,stroke-width:2px;
    classDef modules fill:#cce5ff,stroke:#004085,stroke-width:1px;
    classDef car fill:#f8d7da,stroke:#721c24,stroke-width:1px;

    %% ----------------------------------------------------
    %% 1. 上位机（无线层）
    %% ----------------------------------------------------
    subgraph Layer1 ["1. 诊断上位机 / 操控端"]
        Client["PC诊断软件 / 手机App"]
    end

    %% ----------------------------------------------------
    %% 独立电源节点
    %% ----------------------------------------------------
    供电("12v 电池及充放电控制板")

    %% ----------------------------------------------------
    %% 2. 核心路由层
    %% ----------------------------------------------------
    subgraph Layer2 ["2. VONETS 模块 / 路由器"]
        WiFi(("Wi-Fi AP 天线"))
        
        subgraph Int_Switch ["路由核心"]
            LAN1["LAN 端口<br/> "]
        end
    end

    %% ----------------------------------------------------
    %% 3. 自制核心板 (MCU主控 + 双层开关)
    %% ----------------------------------------------------
    subgraph Layer3 ["3. 自制核心控制板 (MCU中枢)"]
        MCU["单片机 (MCU) <br/> 接收串口透传命令"]
        Eth_Mux["高速以太网开关芯片"]
        Can_Mod["CAN-FD 转网口模块"]
        Net_Trans["网络变压器 <br/> (DoIP 物理隔离)"]
        OBD_Mux["信号双向模拟开关"]
        Act_Driver["12V 强电激活驱动电路"]
    end

    %% ----------------------------------------------------
    %% 4. 车辆物理接口层
    %% ----------------------------------------------------
    subgraph Layer5 ["4. 汽车 OBD-II 物理接口"]
        OBD_P6_14["OBD 针脚 6/14 <br/> (CAN_H / L 信号)"]
        OBD_P12_13["OBD 针脚 12/13 <br/> (DoIP TX 差分)"]
        OBD_P3_11["OBD 针脚 3/11 <br/> (BCAN / DoIP RX 选通)"]
        OBD_P8["OBD 针脚 8 <br/> (12V 强电激活)"]
        OBD_P16["OBD 针脚 16 <br/> (汽车常电 12V)"]
    end

    %% ----------------------------------------------------
    %% 链路连接
    %% ----------------------------------------------------
    %% 电源分配线
    供电 --> Layer2
    供电 --> Layer3

    Client <-->|无线连接| WiFi
    WiFi <-->|网络总线| Int_Switch
    
    %% 串口控制链
    WiFi -.->|串口透传数据| MCU

    %% MCU 控制两条开关线
    MCU -->|GPIO 控制线 1| Eth_Mux
    MCU -->|GPIO 控制线 2| OBD_Mux
    MCU -->|GPIO 控制线 3| Act_Driver

    %% 唯一的 LAN1 口接入网络开关
    LAN1 <-->|以太网 4 线| Eth_Mux
    
    %% 网络开关的两个去向
    Eth_Mux <-->|通道 A| Can_Mod
    Eth_Mux <-->|通道 B| Net_Trans

    %% OBD 开关选通及最终引脚连接
    Can_Mod <--> OBD_P6_14
    Can_Mod -.->|BCAN 信号| OBD_Mux
    Net_Trans <--> OBD_P12_13
    Net_Trans -.->|DoIP RX 信号| OBD_Mux

    OBD_Mux <--> OBD_P3_11
    Act_Driver --> OBD_P8
    OBD_P16 --> Act_Driver

    %% 类应用样式
    class Client user;
    class WiFi,Int_Switch,LAN1 router;
    class MCU,Eth_Mux,Can_Mod,Net_Trans,OBD_Mux,Act_Driver modules;
    class OBD_P8,OBD_P3_11,OBD_P6_14,OBD_P12_13,OBD_P16 car;
