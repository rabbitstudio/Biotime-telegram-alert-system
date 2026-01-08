## Diagram #1 — Data Plane (Packet Flow: Site A → MPLS → Site B)

```mermaid
flowchart LR
  subgraph A["Site A (LAN)"]
    PC["Client/PC\n(Host A)"]
    CE_A["CE Router / FW\n(Default Gateway)"]
  end

  subgraph SP["Service Provider MPLS (Interlink)"]
    PE_A["PE (Provider Edge)\nVRF: VPN1"]
    P1["P Router (Core)"]
    P2["P Router (Core)"]
    PE_B["PE (Provider Edge)\nVRF: VPN1"]
  end

  subgraph B["Site B (LAN)"]
    CE_B["CE Router / FW"]
    SV["Server\n(Host B)"]
  end

  PC -->|"1) IP packet to GW"| CE_A
  CE_A -->|"2) Lookup route → next-hop to MPLS"| PE_A
  PE_A -->|"3) Push MPLS label\n(enter L3VPN/VRF VPN1)"| P1
  P1 -->|"4) Label switch"| P2
  P2 -->|"4) Label switch"| PE_B
  PE_B -->|"5) Pop label\n(exit VRF VPN1)"| CE_B
  CE_B -->|"6) Forward in LAN"| SV

  CE_A -.->|"Access link 10/20 Mbps"| PE_A
  PE_B -.->|"Access link 10/20 Mbps"| CE_B
