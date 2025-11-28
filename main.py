import cv2
import numpy as np

def place_image_matcher(img_path1, img_path2, min_match_count=15, output_matches="track_avancado_resultado.png"):
   img1 = cv2.imread(img_path1, cv2.IMREAD_COLOR)
   img2 = cv2.imread(img_path2, cv2.IMREAD_COLOR)

   if img1 is None or img2 is None:
      print("Erro: Não foi possível carregar uma ou ambas as imagens. Verifique o caminho e nome dos arquivos.")
      exit()

   gray1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
   gray2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)

   sift = cv2.SIFT_create()
   kp1, des1 = sift.detectAndCompute(gray1, None)
   kp2, des2 = sift.detectAndCompute(gray2, None)

   if des1 is None or des2 is None or len(kp1) < 2 or len(kp2) < 2:
      print("Atenção: Poucos keypoints detectados para comparação robusta.")
      return False, 0

   des1 = np.float32(des1)
   des2 = np.float32(des2)

   index_params = dict(algorithm=1, trees=5)
   search_params = dict(checks=50)
   flann = cv2.FlannBasedMatcher(index_params, search_params)

   matches = flann.knnMatch(des1, des2, k=2)

   good_matches = []
   for m, n in matches:
      if m.distance < 0.75 * n.distance:
         good_matches.append(m)

   if len(good_matches) < 4:
      print(f"❌ Matches após Lowe Test insuficientes ({len(good_matches)}). Mínimo exigido: 4.")
      return False, 0

   pts1 = np.float32([kp1[m.queryIdx].pt for m in good_matches]).reshape(-1, 1, 2)
   pts2 = np.float32([kp2[m.trainIdx].pt for m in good_matches]).reshape(-1, 1, 2)

   H, mask = cv2.findHomography(pts1, pts2, cv2.RANSAC, 5.0)

   inliers_mask = mask.ravel().tolist()
   inlier_matches = [m for i, m in enumerate(good_matches) if inliers_mask[i] == 1]
   
   inlier_count = len(inlier_matches)
   
   print(f"\nMatches após Lowe Test: {len(good_matches)}")
   print(f"✅ Inliers (Pontos Validados): {inlier_count}")

   resultado = cv2.drawMatches(
        img1, kp1,
        img2, kp2,
        inlier_matches,
        None,
        flags=cv2.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS
   )

   cv2.imwrite(output_matches, resultado)
   print(f"🖼️ Imagem do track salva como: {output_matches}")

   mesmo_local = inlier_count >= min_match_count
   
   if mesmo_local:
      print(f"➡️ DECISÃO: As imagens SÃO do mesmo local (Inliers: {inlier_count} / Mínimo: {min_match_count}).")
   else:
      print(f"➡️ DECISÃO: As imagens NÃO são do mesmo local (Inliers: {inlier_count} / Mínimo: {min_match_count}).")
      
   return mesmo_local, inlier_count

place_image_matcher('colonia1.jpg', 'colonia2.jpg', 10)