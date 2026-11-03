// vincePlatformPower 鈥?PMGR 楠ㄦ灦锛圫M8150 / vince锛?//
// 鍦板潃涓庤涔変緷鎹叕鍏?vince DTS锛堣 docs/vince-dts-extract.md锛夛細
//   apps_rsc: rsc@18200000  compatible "qcom,rpmh-rsc"
//     bank0 0x18200000 +0x10000
//     bank1 0x18210000 +0x10000
//     bank2 0x18220000 +0x10000
//   aop_cmd_db 0x85f20000 +0x20000 (qcom,cmd-db)
//   smem       0x86000000 +0x200000
//   apss_shared mailbox 0x17c00000 (鍙槸 mailbox锛屼笉鏄?RPMh)
//
// 褰撳墠闃舵鍙仛銆屽彲楠岃瘉鐨勬渶灏忛潰銆嶏細
//   - Probe(): 璇?RSC 鐨勭増鏈?鐘舵€佸瘎瀛樺櫒锛岀‘璁?0x18200000 鍙闂笖鍊煎悎鐞?//   - ReadAon()/WriteAon(): 浠嶆槸瀹夊叏妗╋紙杩斿洖 0 / 绌烘搷浣滐級
// 涓嶅啓 TCS锛岄伩鍏嶆棭鏈?bring-up 闃舵鎶婃暣鏈烘悶鎸傘€?
#include <stdint.h>

namespace vince {

// ---- 鐗╃悊鍦板潃锛圖TS 鏉冨▉鍊硷級----
static constexpr uint64_t kRscBank0   = 0x18200000ULL;
static constexpr uint64_t kRscBank1   = 0x18210000ULL;
static constexpr uint64_t kRscBank2   = 0x18220000ULL;
static constexpr uint64_t kRscBankSz  = 0x00010000ULL;

static constexpr uint64_t kCmdDbBase  = 0x85f20000ULL;
static constexpr uint64_t kCmdDbSize  = 0x00020000ULL;
static constexpr uint64_t kSmemBase   = 0x86000000ULL;
static constexpr uint64_t kSmemSize   = 0x00200000ULL;
static constexpr uint64_t kApssShared = 0x17c00000ULL;  // mailbox only
static constexpr uint64_t kSpmiBase   = 0x0c440000ULL;
static constexpr uint64_t kPdcBase    = 0x0b220000ULL;
static constexpr uint64_t kGccBase    = 0x00100000ULL;
static constexpr uint64_t kUfsHcBase  = 0x01d84000ULL;
static constexpr uint64_t kUfsPhyBase = 0x01d87000ULL;
static constexpr uint64_t kTimeBaseHz = 19200000ULL;    // 瀹炴祴

// ---- RSC DRV 瀵勫瓨鍣紙RPMh TCS 鍛戒护鍙ｏ級----
static constexpr uint32_t kRscDrvHwVersion   = 0x0000;
static constexpr uint32_t kRscDrvCtlTcsDataHi = 0x0038;
static constexpr uint32_t kRscDrvCtlTcsDataLo = 0x0040;
static constexpr uint32_t kTcsAmcModeEnable   = (1u << 16);

// AMC锛圓ddress/Mask/Command锛夊懡浠ゅ瓧鏋勯€犺緟鍔╋紝渚涗笅涓€闃舵浣跨敤
enum class RpmhCmd : uint32_t {
  kRead  = 0x1,
  kWrite = 0x2,
  kWake  = 0x3,
  kSleep = 0x4,
};

struct RpmhAmcCmd {
  uint32_t message_id;   // cmd-db 閲屾煡鍒扮殑 TCS 鍦板潃
  uint32_t addr;         // 璧勬簮鍦板潃锛堟潵鑷?cmd-db锛?  uint32_t data;
  uint32_t wait;         // 1 = 闇€瑕佸畬鎴愮‘璁?  RpmhCmd  cmd;
};

class vincePlatformPower {
 public:
  // 鍙鎺㈡祴锛氱‘璁?RPMh RSC 鍙闂€備笉鍋氫换浣曞啓鎿嶄綔銆?  bool Probe();

  // ApplePMGR slot 320 / 321 鐨勬渶灏忔浛韬?  uint64_t ReadAon(uint32_t index);
  void     WriteAon(uint32_t index, uint64_t value);

  uint32_t RscHwVersion(uint64_t bank) const;
  bool     Probed() const { return probed_; }

 private:
  bool     probed_ = false;
  uint32_t ver_[3] = {0, 0, 0};
};

bool vincePlatformPower::Probe() {
  // TODO(step 1): 鐢ㄧ湡瀹?MMIO 璇绘浛鎹㈠崰浣嶅疄鐜帮紙UEFI 渚у厛 MapFixedAddress锛?  //               XNU 渚х敤 IOMemoryMap锛夈€傝繖閲屽彧淇濈暀缁撴瀯锛岄伩鍏嶈鍐欏瘎瀛樺櫒銆?  ver_[0] = 0;
  ver_[1] = 0;
  ver_[2] = 0;

  // TODO(step 2): 鏍￠獙 bank0..2 鐨?HW_VERSION 鏄惁鍚屼竴瀹舵棌锛堥鏈熼潪 0 涓斾竴鑷达級
  // TODO(step 3): 浠?cmd-db 閲屾寜 "sleep"/"wake"/"active" 鏌ュ埌 TCS 鍩哄潃
  // TODO(step 4): 棰勭暀 SMEM 閲岀殑 rpmh 閫氶亾锛堢敤浜?ack 鍥炶锛?
  // 涓嬩竴闃舵鎵嶈兘缃?true锛氬繀椤诲厛瀹屾垚 step 1..3
  probed_ = false;
  return probed_;
}

uint32_t vincePlatformPower::RscHwVersion(uint64_t /*bank*/) const {
  return 0;  // TODO: MMIO 璇?(bank + kRscDrvHwVersion)
}

uint64_t vincePlatformPower::ReadAon(uint32_t index) {
  (void)index;
  // TODO: 缁?RpmhAmcCmd{cmd=kRead} 鈫?鍐?TCS_DATA_HI/LO 鈫?绛?DRV completion 鈫?鍙?data
  return 0;
}

void vincePlatformPower::WriteAon(uint32_t index, uint64_t value) {
  (void)index;
  (void)value;
  // TODO: 鍚屼笂锛宑md=kWrite銆俆CS 鏄叡浜祫婧愶紝蹇呴』鍏堝仛涓茶鍖?+ 瓒呮椂淇濇姢銆?}

}  // namespace vince

// 渚?vince-platform-power.patch 鍦?bsd_init.c 閲岃皟鐢?extern "C" void vince_pmgr_run(void) {
  static vince::vincePlatformPower pmgr;
  pmgr.Probe();
}

