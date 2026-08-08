/* vi: set sw=4 ts=4:
 *
 * Copyright (C) 2015 Christian Hohnstaedt.
 *
 * All rights reserved.
 */

#include <QPixmap>
#include "XcaDialog.h"
#include "MainWindow.h"
#include "Help.h"

#include <QLabel>
#include <QHBoxLayout>
#include <QSizePolicy>

// index = enum pki_type
static const char * const PixmapMap[] = {
    "", ":keyImg", ":csrImg", ":certImg", ":revImg", ":tempImg", "", ":scardImg",
};

XcaDialog::XcaDialog(QWidget *parent, enum pki_type type, QWidget *w,
			const QString &t, const QString &desc,
			const QString &help_ctx)
	 : QDialog(parent ? parent : mainwin)
{
	setupUi(this);
	setWindowTitle(XCA_TITLE);
	image->setPixmap(QPixmap(PixmapMap[type]));
	content->addWidget(w);
	mainwin->helpdlg->register_ctxhelp_button(this, help_ctx);

	widg = w;
	title->setText(t);
	if (desc.isEmpty()) {
		verticalLayout->removeWidget(description);
		delete description;
	} else {
		description->setText(desc);
	}
}

void XcaDialog::noSpacer()
{
	verticalLayout->removeItem(topSpacer);
	verticalLayout->removeItem(bottomSpacer);
	delete topSpacer;
	delete bottomSpacer;
	if (widg)
		widg->setSizePolicy(QSizePolicy::Expanding,
					QSizePolicy::Expanding);
}

void XcaDialog::aboutDialog(const QPixmap &left)
{
	title->setPixmap(left.scaledToHeight(title->height()));
	noSpacer();
	resize(560, 400);
	buttonBox->setStandardButtons(QDialogButtonBox::Ok);
	buttonBox->centerButtons();
}

void XcaDialog::aboutDialog(const QPixmap &left, const QPixmap &middle)
{
	// 先调用单参数版本，设置左侧图片
	aboutDialog(left);

	// 1. 找到包含 title 的水平布局 (QHBoxLayout)
	QHBoxLayout *hbox = nullptr;
	QLayout *topLayout = this->layout(); // 获取最外层布局
	if (topLayout) {
		for (int i = 0; i < topLayout->count(); ++i) {
			QLayoutItem *item = topLayout->itemAt(i);
			QHBoxLayout *h = qobject_cast<QHBoxLayout*>(item->layout());
			if (h && h->indexOf(title) != -1) {
				hbox = h;
				break;
			}
		}
	}

	if (hbox) {
		// 2. 创建中间图片标签，并限制最大大小为 150x100，按比例缩放
		QLabel *midLabel = new QLabel(this);
		QPixmap midPix = middle.scaled(150, 100, Qt::KeepAspectRatio, Qt::SmoothTransformation);
		midLabel->setPixmap(midPix);
		midLabel->setAlignment(Qt::AlignCenter);
		midLabel->setSizePolicy(QSizePolicy::Preferred, QSizePolicy::Fixed);

		// 3. 将标签插入到 title 之后，并在两侧加上弹性因子实现居中
		int idx = hbox->indexOf(title);
		hbox->insertWidget(idx + 1, midLabel);
		hbox->insertStretch(idx + 1, 1); // 左侧弹性
		hbox->insertStretch(idx + 3, 1); // 右侧弹性
	}
}
