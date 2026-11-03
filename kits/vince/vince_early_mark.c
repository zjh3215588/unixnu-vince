// 瀹炵幇锛氬彧鍋氭櫘閫氬唴瀛樺啓锛坆ase + rowBytes*y + 4*x锛夛紝涓嶇浠讳綍瀵勫瓨鍣紝
// 涓嶅仛鍐呭瓨鍒嗛厤锛屽け璐ョ粷涓?panic 鈥斺€?鏈€鍧忔儏鍐靛氨鏄睆骞曚笂浠€涔堜篃涓嶅銆?//
// 杩欎唤鏂囦欢涓?UniXNU/scripts/build-xnu-4k-baseline.sh 鍐呰仈鐨?MKC / MKH 淇濇寔涓€鑷?// 锛圕I 鐢ㄧ殑鏄偅浠藉唴鑱旂増鏈紝鏈洰褰曟槸甯︽敞閲婄殑闀滃儚婧愶級銆?
#include "vince_early_mark.h"
#include <stddef.h>

static volatile unsigned int *g_fb = NULL;
static unsigned long g_px = 0;      // 姣忚鍍忕礌鏁?= rowBytes / 4
static unsigned int  g_w  = 0;
static unsigned int  g_h  = 0;
static int           g_slot = 0;    // 涓嬩竴涓爣璁扮敾鍦ㄧ鍑犳Ы

static void fill(unsigned int x0, unsigned int y0, unsigned int w, unsigned int h, unsigned int c)
{
	unsigned int x, y, xe = x0 + w, ye = y0 + h;
	if (g_fb == NULL) {
		return;
	}
	if (xe > g_w) {
		xe = g_w;
	}
	if (ye > g_h) {
		ye = g_h;
	}
	for (y = y0; y < ye; y++) {
		for (x = x0; x < xe; x++) {
			g_fb[(unsigned long)y * g_px + x] = c;
		}
	}
}

static int sane(unsigned long row, unsigned long w, unsigned long h)
{
	return row >= 4 && row <= 65536 && w >= 1 && w <= 8192 && h >= 1 && h <= 8192;
}

void vince_mark_init(const unsigned long *v)
{
	unsigned long row, w, h;
	int fallback = 0;

	g_fb = NULL;
	g_px = 0;
	g_w = 0;
	g_h = 0;
	g_slot = 0;

	if (v == NULL || v[0] == 0) {
		return;                 // 娌℃湁甯х紦鍐诧細闈欓粯鏀惧純
	}

	// struct Boot_Video 椤哄簭锛歜ase, display, rowBytes, width, height, depth
	row = v[2];
	w   = v[3];
	h   = v[4];
	if (!sane(row, w, h)) {
		// 鏃ф暟缁勯『搴忥細base, rowBytes, width, height, depth, display
		row = v[1];
		w   = v[2];
		h   = v[3];
		fallback = 1;
		if (!sane(row, w, h)) {
			// 鍑犱綍淇℃伅瀹屽叏涓嶅彲鐢紝浣?base 鐪嬬潃鍙啓锛?			// 鐢讳竴灏忓潡绾㈢偣锛岃銆屽抚缂撳啿娌℃槧灏勩€嶅拰銆屾槧灏勪簡浣嗗弬鏁版槸鍨冨溇銆嶅彲鍖哄垎
			g_fb = (volatile unsigned int *)(unsigned long)v[0];
			g_px = 4096;
			g_w  = 4096;
			g_h  = 4096;
			fill(0, 0, 16, 16, 0xFFFF0000);
			g_fb = NULL;
			return;
		}
	}

	g_fb = (volatile unsigned int *)(unsigned long)v[0];
	g_px = row / 4;
	g_w  = (unsigned int)w;
	g_h  = (unsigned int)h;

	// 鍏堥摵涓€鏉￠粦搴曪紝淇濊瘉鑹插潡瀵规瘮搴?	fill(0, 0, g_w, 112, 0xFF000000);

	// 鑻ヨ蛋浜?fallback锛堟垨 depth 涓嶆槸 32bpp锛夛紝鍦ㄦí鏉℃渶鍙崇敾绾㈠潡鎻愮ず甯冨眬鏈夐棶棰?	if (fallback || (v[5] & 0xFF) != 32) {
		fill(32 + 7 * 64, 32, 48, 48, 0xFFFF0000);
	}
}

void vince_mark(int n)
{
	static const unsigned int colors[9] = {
		0,          // 0 鏈敤
		0xFFFFFFFF, // 1 鐧?		0xFFFFFF00, // 2 榛?		0xFF00FFFF, // 3 闈?		0xFF00FF00, // 4 缁?		0xFFFF00FF, // 5 鍝佺孩
		0xFFFF8000, // 6 姗?		0xFF0000FF, // 7 钃?		0xFFFF0000, // 8 绾紙鎶ラ敊涓撶敤锛?	};

	if (g_fb == NULL || n < 1 || n > 8 || g_slot >= 8) {
		return;
	}
	fill(32 + (unsigned int)g_slot * 64, 32, 48, 48, colors[n]);
	g_slot++;
}

