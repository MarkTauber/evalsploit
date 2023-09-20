<?php
ob_start();
session_start();
include "params/connect.php";
include "params/function.php";
include "config.php";
include "heading.php";
$TITLE = SITE_TITLE; 
$DESCRIPTION = DD1;
$KEYWORDS = KK1;
include "meta.php";
include "header.php";
?>

<div class="item content">
	<div class="container toparea">
		<div class="row text-center">
			<div class="col-md-4">
				<div class="col editContent">
					<span class="numberstep"><i class="fa fa-shopping-cart"></i></span>
					<h3 class="numbertext"><?=HH150?></h3>
					<p>
						<?=HH151?><br />
						<?=HH152?> <a href="tel:<?=HH153?>"><?=HH149?></a>
					</p>
				</div>
				<!-- /.col-md-4 -->
			</div>
			<!-- /.col-md-4 col -->
			<div class="col-md-4 editContent">
				<div class="col">
					<span class="numberstep"><i class="fa fa-send"></i></span>
					<h3 class="numbertext"><?=HH154?></h3>
					<p><?=HH155?></p>
				</div>
				<!-- /.col -->
			</div>
			<!-- /.col-md-4 col -->
			<div class="col-md-4 editContent">
				<div class="col">
					<span class="numberstep"><i class="fa fa-phone"></i></span>
					<h3 class="numbertext"><?=HH156?></h3>
					<p>
						<?=HH157?><br /><?=HH158?>
					</p>
				</div>
			</div>
		</div>
	</div>
</div>

<section class="item content">
	<div class="container">
		<div class="underlined-title">
			<div class="editContent">
				<h1 class="text-center latestitems"><?=HH159?></h1>
			</div>
			<div class="wow-hr type_short">
				<span class="wow-hr-h">
				<i class="fa fa-star"></i>
				<i class="fa fa-star"></i>
				<i class="fa fa-star"></i>
				<i class="fa fa-star"></i>
				<i class="fa fa-star"></i>
				</span>
			</div>
		</div>
		<div class="row">
		
			<?php
			$listTopics = db_array(mysql_query("SELECT * FROM `".PREFIX."topics` WHERE `status` = '0' ORDER BY `psort` ASC, `id` ASC LIMIT 3"));
			foreach($listTopics as $lt) 
			{ 
				?>
				<div class="col-md-4">
					<div class="productbox">
						<div class="fadeshop">
							<div class="captionshop text-center" style="display: none;">
								<h3><?=$lt['title']?></h3>
								<p><?=HH163?></p>
								<p>
									<a href="#animatedModal" class="orderOnline learn-more detailslearn orderOnline" rel="<?=HH162?> <?=$lt['title']?>"><i class="fa fa-shopping-cart"></i> <?=HH160?></a>
									<a href="catalog.html?c=<?=$lt['seo_id']?>" class="learn-more detailslearn"><i class="fa fa-link"></i> <?=HH161?></a>
								</p>
							</div>
							<span class="maxproduct"><img src="filez/<?=$lt['image']?>" alt=""></span>
						</div>
						<div class="product-details">
							<a href="catalog.html?c=<?=$lt['seo_id']?>">
							<h1><?=$lt['title']?></h1>
							</a>
							<span class="price">
							<span class="edd_price"><?=$lt['txt']?></span>
							</span>
						</div>
					</div>
				</div>
				<?php
			}
			?>
		</div>
	</div>
</div>
</section>

<div class="item content">
	<div class="container text-center">
		<a class="orderOnline homebrowseitems orderOnline" href="#animatedModal" rel=""><?=HH164?>
		<div class="homebrowseitemsicon">
			<i class="fa fa-star fa-spin"></i>
		</div>
		</a>
	</div>
</div>
<br/>

<div class="item content">
	<div class="container">
		<div class="row">
			<div class="col-md-4">
				<i class="fa fa-globe infoareaicon"></i>
				<div class="infoareawrap">
					<h1 class="text-center subtitle"><?=HH165?></h1>
					<p><?=HH166?></p>
				</div>
			</div>
			<!-- /.col-md-4 col -->
			<div class="col-md-4">
				<i class="fa fa-comments infoareaicon"></i>
				<div class="infoareawrap">
					<h1 class="text-center subtitle"><?=HH167?></h1>
					<p><?=HH168?></p>
				</div>
			</div>
			<!-- /.col-md-4 col -->
			<div class="col-md-4">
				<i class="fa fa-bullhorn infoareaicon"></i>
				<div class="infoareawrap">
					<h1 class="text-center subtitle"><?=HH169?></h1>
					<p><?=HH170?></p>
				</div>
			</div>
		</div>
	</div>
</div>

<div class="item content">
	<div class="container">
		<div class="col-md-10 col-md-offset-1">
			<div class="slide-text">
				<div>
					<h2><span class="uppercase"><?=HH171?></span></h2>
					<img src="images/budstudabout.jpg" alt="<?=HH171?>">
					<?=PageEcho("pages",'ids','61','1');?>
					<i class="fa fa-star"></i><i class="fa fa-star"></i><i class="fa fa-star"></i><i class="fa fa-star"></i><i class="fa fa-star"></i>
				</div>
			</div>
		</div>
	</div>
</div>

<?php 
include "oform.php";
include "footer.php";