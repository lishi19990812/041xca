/* vi: set sw=4 ts=4:
 *
 * Copyright (C) 2001 - 2020 Christian Hohnstaedt.
 *
 * All rights reserved.
 */


#include "MainWindow.h"
#include <QApplication>
#include <QMimeData>
#include <QPixmap>
#include <QLabel>
#ifndef OPENSSL_NO_EC
#include <openssl/ec.h>
#endif
#include "XcaDialog.h"
#include "ui_Help.h"
#include "lib/func.h"
#include "lib/entropy.h"

const QList<QStringList> MainWindow::getTranslators() const
{
	return QList<QStringList> {
	QStringList{ "", tr("System") },
	QStringList{ "bg", tr("Bulgarian"), "Svetoslav Slavkov", "contact", "sslavkov.eu" },
	QStringList{ "zh_CN", tr("Chinese"), "Xczh", "xczh.me", "foxmail.com" },
	QStringList{ "hr", tr("Croatian"), "Nevenko Bartolincic", "nevenko.bartolincic", "gmail.com" },
	QStringList{ "nl", tr("Dutch"), "Guido Pennings" },
	QStringList{ "en", tr("English") },
	QStringList{ "fr", tr("French"), "Patrick Monnerat", "patrick", "monnerat.net" },
	QStringList{ "de", tr("German"), "Christian Hohnstädt", "christian", "hohnstaedt.de" },
	QStringList{ "id", tr("Indonesian"), "Andika Triwidada", "andika", "gmail.com" },
	QStringList{ "it", tr("Italian"), "Paolo Basenghi", "paul69", "libero.it" },
	QStringList{ "ja", tr("Japanese"), "D2N", "gritty.hat3143", "mx.d2-networks.jp" },
	QStringList{ "fa", tr("Persian"), "Erfan Esmayili Barzi", "erfankam", "gmail.com" },
	QStringList{ "ko", tr("Korean"), "Kim Dongil", "icoicoya", "naver.com" },
	QStringList{ "pl", tr("Polish"), "Jacek Tyborowski", "jacek", "tyborowski.pl" },
	QStringList{ "pt_BR", tr("Portuguese in Brazil"), "Ulisses Guedes", "uli1958", "hotmail.com" },
	QStringList{ "ru", tr("Russian") },
	QStringList{ "sk", tr("Slovak"), "Slavko", "linux", "slavino.sk" },
	QStringList{ "es", tr("Spanish"), "Miguel Romera", "mrmsoftdonation", "gmail.com" },
	QStringList{ "tr", tr("Turkish") },
	};
};

void MainWindow::about()
{
	QTextEdit *textbox = new QTextEdit(NULL);
	XcaDialog *about = new XcaDialog(this, x509, textbox,
					QString(), QString());
about->aboutDialog(QPixmap(":scardImg"), QPixmap(":lsy041Img"));
	QString openssl, qt, cont, version, brainpool;
#ifdef OPENSSL_NO_EC
	brainpool = "(Elliptic Curve Cryptography support disabled)";
#endif
	openssl = SSLeay_version(SSLEAY_VERSION);
	qt = qVersion();
	if (openssl != OPENSSL_VERSION_TEXT ||
	    qt != QT_VERSION_STR)
	{
		version = QString("<table border=0 width=500><tr>"
				"<td>Compile time:</td>"
				"<td>" OPENSSL_VERSION_TEXT "</td>"
				"<td>QT version: " QT_VERSION_STR "</td>"
				"</tr><tr>"
				"<td>Run time:</td>"
				"<td>%1</td>"
				"<td>QT version: %2</td>"
				"</tr></table>").arg(openssl).arg(qt);
	} else {
		version = QString("%1<br>QT version: %2").arg(openssl).arg(qt);
	}
	QStringList rows;
	foreach(QStringList sl, getTranslators()) {
		QString email;
		QStringList tag { "<td>", "</td>" };
		if (sl.size() < 3)
			continue;
		if (sl.size() > 4)
			email = QString("<%1@%2>").arg(sl[3]).arg(sl[4]);
		QString lang(QLocale::languageToString(QLocale(sl[0]).language()));
		QStringList row {
			QString("<b>%1</b>").arg(lang),
			sl[2].toHtmlEscaped(),
			email.toHtmlEscaped(),
		};
		rows << tag[0] + row.join(tag[0] + tag[1]) + tag[1];
	}

	Entropy::seed_rng();
	cont = QString(
	"<p><h1><center>041专属 - XCA</center></h1></p>"
	"<p><h3><center>Copyright 041专属 © All Rights Reserved</center></h3></p>"
	"<p>来源版本：XCA - %1%2</p>"
	"<p>编译程序："
	"OpenSSL：%3、"
	"Qt：%4、"
	"VS：Visual Studio 2026</p>"
	"<p>邮&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;箱：<u>mynameis041@vip.qq.com</u></p>"
	"<p>个人主页：<a href=\"https://www.lsy041.com\">https://www.lsy041.com</a></p>"
	"<p>开源地址：<a href=\"https://github.com/lishi19990812/041xca\">https://github.com/lishi19990812/041xca</a></p>"
	"<p>XCA官网：<a href=\"https://hohnstaedt.de/xca\">https://hohnstaedt.de/xca</a></p>"
	
	"<p><th align=left>ps:</th>修复翻译了一些中文语言包未翻译的字符，在创建证书界面添加了自定义序列号的选项，添加了SM2密钥创建、SM3哈希算法、SM4的对称加密。</p>"
	
	"<hr><table border=\"0\">"
	"<tr><th align=left>Christian Hohnst&auml;dt</th><td><u>&lt;christian@hohnstaedt.de&gt;</u></td></tr>"
	"<tr><td></td><td>Programming, Translation and Testing</td></tr>"
	"<tr><th align=left>Kerstin Steinhauff</th><td><u>&lt;tine@kerstine.de&gt;</td></u></tr>"
	"<tr><td></td><td>Arts and Graphics</td></tr>"
	"<tr><th align=left>XCA Copyright</th><td> <p>Copyright 2001 - 2024 by Christian Hohnstädt</p>"
	"</table><hr><center><u><b>Maintained Translations</b></u></center>"
	"<p><table><tr>%5</tr></table>")
			.arg(version_str(true))                          // %1
#ifndef APPSTORE_COMPLIANT
			.arg(portable_app() ? " (Portable)" : "")       // %2
#else
			.arg(" (App Store)")                            // %2
#endif
			.arg(openssl)                                    // %3
			.arg(qt)                                         // %4
			.arg(rows.join("</tr><tr>"));                    // %5

	textbox->setHtml(cont);
	textbox->setReadOnly(true);
	about->exec();
	delete about;
}
