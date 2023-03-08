#ifndef DEFINES_H
#define DEFINES_H

// Board: Arduino Uno or Arduino Mega
#include <Arduino.h>
#include <avr/wdt.h>

#if defined (__AVR_ATmega328P__) || defined (__AVR_ATmega328__) // Arduino Uno hardware I2C pins
    #define SDA_PORT PORTC
    #define SDA_PIN 4
    #define SCL_PORT PORTC
    #define SCL_PIN 5

#elif defined (__AVR_ATmega1280__) || defined (__AVR_ATmega2560__) // Arduino Mega hardware I2C pins
    #define SDA_PORT PORTD
    #define SDA_PIN 1
    #define SCL_PORT PORTD
    #define SCL_PIN 0

#else // for other boards select I2C-pins here
    #define SDA_PORT PORTC
    #define SDA_PIN 4
    #define SCL_PORT PORTC
    #define SCL_PIN 5
#endif

#define I2C_PULLUP 1 // enable internal pullup resistors for I2C-pins
#define I2C_SLOWMODE 1 // 25 kHz
#define I2C_NOINTERRUPT 1 // interrupts may interfere with SMBus operations
#include <SoftI2CMaster.h> // https://github.com/felias-fogg/SoftI2CMaster

#define ManufacturerAccess          0x00
#define RemainingCapacityAlarm      0x01
#define RemainingTimeAlarm          0x02
#define BatteryMode                 0x03
#define AtRate                      0x04
#define AtRateTimeToFull            0x05
#define AtRateTimeToEmpty           0x06
#define AtRateOK                    0x07
#define Temperature                 0x08
#define Voltage                     0x09
#define Current                     0x0a
#define AverageCurrent              0x0b
#define MaxError                    0x0c
#define RelativeStateOfCharge       0x0d
#define AbsoluteStateOfCharge       0x0e
#define RemainingCapacity           0x0f
#define FullChargeCapacity          0x10
#define RunTimeToEmpty              0x11
#define AverageTimeToEmpty          0x12
#define AverageTimeToFull           0x13
#define ChargingCurrent             0x14
#define ChargingVoltage             0x15
#define BatteryStatus               0x16
#define CycleCount                  0x17
#define DesignCapacity              0x18
#define DesignVoltage               0x19
#define SpecificationInfo           0x1a
#define ManufactureDate             0x1b
#define SerialNumber                0x1c
#define ManufacturerName            0x20
#define DeviceName                  0x21
#define DeviceChemistry             0x22
#define ManufacturerData            0x23

//#define Authenticate               0x2f // baett vid ??????


//#define Unknown_38                  0x38 // probably Cellvoltage4
//#define Unknown_39                  0x39 // probably CellVoltage3
//#define Unknown_3a                  0x3a // probably CellVoltage2
//#define Unknown_3b                  0x3b // probably CellVoltage1

#define CellVoltage4                0x3c
#define CellVoltage3                0x3d
#define CellVoltage2                0x3e
#define CellVoltage1                0x3f

#define BTPDischargeSet             0x4a
#define BTPChargeSet                0x4b
#define StateOfHealth               0x4f

#define SetROMAddress               0x40 // word write only
#define PeekROMByte                 0x42
#define PeekROMBlock                0x43 // block read, size seems to be always 0x20 (32 bytes)
#define FETControl                  0x46

#define SafetyAlert                 0x50 // Block 
#define SafetyStatus                0x51 // Block 
#define PFAlert                     0x52 // Block 
#define PFStatus                    0x53 // Block 
#define OperationStatus             0x54 // Block 
#define ChargingStatus              0x55 // Block 
#define GaugingStatus               0x56 // baett vid Block
//#define ResetData                   0x57
#define ManufacturingStatus         0x57 // baett vid Block
//#define WDResetData                 0x58
//#define AFERegister                 0x58 // baett vid (skrytid) ???????
#define MaxTurboPwr                 0x59 // baett vid (skrytid) ???????

//#define PackVoltage                 0x5a
#define SusTurboPwr                 0x5a // baett vid (skrytid) ???????
#define TURBO_PACK_R                0x5b // baett vid (skrytid)
#define TURBO_SYS_R                 0x5c // baett vid (skrytid)


//#define AverageVoltage              0x5d
//#define TS1Temperature              0x5e
//#define TS2Temperature              0x5f

#define TURBO_EDV                   0x5d // baett vid (skrytid)
#define MaxTurboCurr                0x5e // baett vid (skrytid)
#define SusTurboCurr                0x5f // baett vid (skrytid)


//#define UnSealKey                   0x60
//#define FullAccessKey               0x61
//#define PFKey                       0x62
//#define AuthenKey3                  0x63
//#define AuthenKey2                  0x64

#define LifetimeDataBlock1          0x60 // baett vid Block
#define LifetimeDataBlock2          0x61 // baett vid Block
#define LifetimeDataBlock3          0x62 // baett vid Block
#define LifetimeDataBlock4          0x63 // baett vid Block
#define LifetimeDataBlock5          0x64 // baett vid Block

//#define AuthenKey1                  0x65
//#define AuthenKey0                  0x66
#define ManufacturerInfo            0x70 // Block

//#define SenseResistor               0x71
//#define TempRange                   0x72
#define DAStatus1                   0x71 // baett vid
#define DAStatus2                   0x72 // baett vid

//#define Timestamp                   0x73
//#define ManufacturerStatus          0x74

#define GaugeStatus1                0x73 // baett vid
#define GaugeStatus2                0x74 // baett vid
#define GaugeStatus3                0x75 // baett vid

//#define DataFlashClass              0x77
//#define DataFlashClassSubClass1     0x78
//#define DataFlashClassSubClass2     0x79
//#define DataFlashClassSubClass3     0x7a

#define CBStatus                   0x76 // baett vid
#define StateOfHealth2             0x77 // baett vid
#define FilteredCapacity           0x78 // baett vid

#define buffer_length               257 // 1 length byte + 256 data byte

// Set (1), clear (0) and invert (1->0; 0->1) bit in a register or variable easily
#define sbi(reg, bit) (reg) |=  (1 << (bit))
#define cbi(reg, bit) (reg) &= ~(1 << (bit))
#define ibi(reg, bit) (reg) ^=  (1 << (bit))

// Packet related stuff
// DATA CODE byte building blocks
// Commands (low nibble (4 bits))
#define reset                   0x00
#define handshake               0x01
#define status                  0x02
#define settings                0x03
#define read_data               0x04
#define write_data              0x05
// 0x06-0x0E reserved


#define ok_error                0x0F

// SUB-DATA CODE byte
// Command 0x02 (status)
#define sd_timestamp            0x01
#define sd_scan_smbus_address   0x02
#define sd_smbus_reg_dump       0x03

// SUB-DATA CODE byte
// Command 0x03 (settings)
#define sd_current_settings     0x01
#define sd_set_sb_address       0x02
#define sd_word_byte_order      0x03

// SUB-DATA CODE byte
// Command 0x04 (read_data)
#define sd_read_byte            0x01
#define sd_read_word            0x02
#define sd_read_block           0x03
#define sd_read_rom_byte        0x04
#define sd_read_rom_block       0x05

// SUB-DATA CODE byte
// Command 0x05 (write_data)
#define sd_write_byte           0x01
#define sd_write_word           0x02
#define sd_write_block          0x03

// SUB-DATA CODE byte
// Command 0x0F (ok_error)
#define ok                                      0x00
#define error_length_invalid_value              0x01
#define error_datacode_invalid_command          0x02
#define error_subdatacode_invalid_value         0x03
#define error_payload_invalid_values            0x04
#define error_checksum_invalid_value            0x05
#define error_packet_timeout_occured            0x06
// 0x07-0xFD reserved
#define error_internal                          0xFE
#define error_fatal                             0xFF

#endif