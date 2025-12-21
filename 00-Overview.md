# 00 - Overview

## Project
**BioTime → Telegram Alert System (Department-based)**

## Problem Statement
HR/IT ต้องตรวจสอบการมาทำงานจากระบบ BioTime แบบ manual และมักรู้ช้าเมื่อมีเหตุการณ์สำคัญ (มาสาย/ขาด/เหตุผิดปกติ)

## Objective
สร้างระบบแจ้งเตือนแบบ near real-time จาก BioTime โดยใช้ไฟล์ CSV export เป็นแหล่งข้อมูล และส่งแจ้งเตือนเข้า Telegram แยกตามแผนก พร้อมสรุปรายวันให้ผู้ดูแล

## Scope
### In-scope
- Monitor ไฟล์ CSV export จาก BioTime (polling)
- ส่งแจ้งเตือน Telegram แยกตาม department
- Daily summary ส่งให้ admin
- Logging + backup trail
- Weekly reset / housekeeping

### Out-of-scope (ปัจจุบัน)
- แก้ไขข้อมูลใน BioTime โดยตรง
- เชื่อมต่อ DB ของ BioTime (ใช้ CSV export เป็นหลัก)
- GUI จัดการ config (วางเป็น next step)

## Environment (example / sanitized)
- On-prem Windows Server + shared folder
- Python runtime (scheduled task / service)
- Telegram Bot API

## Key Deliverables
- Repo documentation (Design/Implementation/Test/Rollback/Lessons Learned)
- Production-ready script structure (config, logging, backup, safe operations)

## Success Criteria
- HR/IT ได้รับแจ้งเตือนถูกต้อง “ตามแผนก” และไม่แจ้งซ้ำผิดพลาด
- Admin ได้ daily summary ทุกวันตามเวลา
- มี log และ backup ตรวจสอบย้อนหลังได้
