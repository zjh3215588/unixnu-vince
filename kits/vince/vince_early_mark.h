// vince_early_mark 鈥?鍐呮牳鏈€鏃╂湡銆岃繘搴︽爣璁般€嶏紝涓嶉渶瑕佸瓧搴撱€佷笉渚濊禆浠讳綍瀛愮郴缁熴€?//
// 璁捐鍔ㄦ満锛氬唴鏍稿湪 PE_create_console 涔嬪墠灏遍潤榛樻浜★紝浠讳綍 console 閮界敤涓嶄笂銆?// 浣?boot_args.Video 宸茬粡缁欏嚭甯х紦鍐诧紙base / rowBytes / width / height / depth锛夛紝
// 鎵€浠ュ唴鏍稿彧瑕佸線鏄惧瓨閲岀敾鍑犲潡鑹插潡锛屽氨鑳芥妸銆屾墽琛屽埌鍝竴姝ャ€嶄紶杈惧埌灞忓箷涓娿€?//
// 鈿狅笍 甯冨眬锛坸nu-10063.141.1 瀹炴祴锛夛細boot_args.Video 涓嶆槸鏁扮粍锛岃€屾槸
//    struct Boot_Video { v_baseAddr; v_display; v_rowBytes; v_width; v_height; v_depth; }
//    娉ㄦ剰 v_display 鍦?*绗?2 涓?* ulong锛乸expert/arm/pe_init.c:419-429 灏辨槸杩欎箞璇荤殑銆?//    鎵€浠ヨ繖閲屾寜銆寀long 瀛楁祦銆嶆帴鏀讹紝鏃㈣兘瀵圭粨鏋勪綋鐢紝涔熻兘鍏煎鏃х殑 [base,rowBytes,...] 鏁扮粍銆?//
// 鐢ㄦ硶锛坅rm_init.c 鏈€鏃╂湡锛夛細
//     vince_mark_init((const unsigned long *)&args->Video);
//     vince_MARK(1);            // arm_init 杩涘叆
//     ...
//
// 璇绘硶锛?//   灞忓箷宸︿笂瑙掑嚭鐜?N 涓壊鍧?鈬?鍐呮牳璧板埌浜嗙 N 涓鏌ョ偣
//   涓€涓兘娌℃湁            鈬?杩?arm_init 閮芥病杩涳紙姝诲湪姹囩紪鍏ュ彛/MMU锛?//   鍙充笂瑙掑嚭鐜?*绾㈣壊鍧?*  鈬?甯х紦鍐插彲鍐欙紝浣?Video 甯冨眬瀵逛笉涓婏紙閿欎綅 / depth 闈?32bpp锛?
void vince_mark_init(const unsigned long *video);
void vince_mark(int n);

// 鏍囪缂栧彿 鈫?棰滆壊锛? 鐧?2 榛?3 闈?4 缁?5 鍝佺孩 6 姗?7 钃?8 绾級
#define vince_MARK(n) vince_mark(n)

