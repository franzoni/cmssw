#ifndef DIGIHGCAL_HGCSAMPLE_H
#define DIGIHGCAL_HGCSAMPLE_H

#include <iostream>
#include <ostream>
#include <cstdint>

/**
   @class HGCSample
   @short wrapper for a data word
 */

class HGCSample {
public:
  enum HGCSampleMasks {
    kThreshMask = 0x1,
    kModeMask = 0x1,
    kToAValidMask = 0x1,
    kGainMask = 0xf,
    kToAMask = 0x3ff,
    kDataMask = 0xfff
  };
  enum HGCSampleShifts {
    kThreshShift = 31,
    kModeShift = 30,
    kToAValidShift = 29,
    kToGainShift = 22,
    kToAShift = 12,
    kDataShift = 0
  };

  /**
     @short CTOR
  */
  HGCSample() : value_(0) {}
  HGCSample(uint32_t value) : value_(value) {}
  HGCSample(const HGCSample& o) : value_(o.value_) {}


  /**
     @short Data Model Evolution
  */
static  uint32_t newForm(uint32_t value, bool toaFired) { 
    // here write the logic to combine value&toaFired 
    // from persisted objects of in V9 (or earlier) format
    // to produce a value_ compatible w/ the V10 format
    // i.e.
    // 1) shift the adc 12 bits by 1 bit
    // 2) insert the toaFired into _value
    return 100;
  }
  /**
     @short setters
  */
  void setThreshold(bool thr) { setWord(thr, kThreshMask, kThreshShift); }
  void setMode(bool mode) { setWord(mode, kModeMask, kModeShift); }
  void setGain(uint16_t gain) { setWord(gain, kGainMask, kToGainShift); }
  void setToA(uint16_t toa) { setWord(toa, kToAMask, kToAShift); }
  void setData(uint16_t data) { setWord(data, kDataMask, kDataShift); }
  void setToAValid(bool toaFired) { setWord(toaFired, kToAValidMask, kToAValidShift); }

  void set(bool thr, bool mode, uint16_t gain, uint16_t toa, uint16_t data) {
    setThreshold(thr);
    setMode(mode);
    setGain(gain);
    setToA(toa);
    setData(data);
  }

  void print(std::ostream& out = std::cout) {
    out << "THR: " << threshold() << " Mode: " << mode() << " ToA: " << toa() << " Data: " << data() << " Raw=0x"
        << std::hex << raw() << std::dec << std::endl;
  }

  /**
     @short getters
  */
  uint32_t raw() const { return value_; }
  bool threshold() const { return getWord(kThreshMask, kThreshShift); }
  bool mode() const { return getWord(kModeMask, kModeShift); }
  uint16_t gain() const { return getWord(kGainMask, kToGainShift); }
  uint16_t toa() const { return getWord(kToAMask, kToAShift); }
  uint16_t data() const { return getWord(kDataMask, kDataShift); }
  bool getToAValid() const { return getWord(kToAValidMask, kToAValidShift); }
  uint32_t operator()() { return value_; }

private:
  /**
     @short wrapper to reset words at a given position
  */
  void setWord(uint16_t word, HGCSampleMasks mask, HGCSampleShifts shift) {
    // mask and shift bits
    const uint32_t masked_word = (word & mask) << shift;

    //clear to 0  bits which will be set by word
    value_ &= ~(mask << shift);

    //now set bits
    value_ |= (masked_word);
  }

  uint32_t getWord(HGCSampleMasks mask, HGCSampleShifts shift) const { return ((value_ >> shift) & mask); }

  // a 32-bit word
  uint32_t value_;
};

#endif
