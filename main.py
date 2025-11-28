import cv2
import numpy as np
import random

def place_image_matcher(img_path1, img_path2, min_match_count=10):
   img1 = cv2.imread(img_path1, cv2.IMREAD_COLOR)
   img2 = cv2.imread(img_path2, cv2.IMREAD_COLOR)

   if img1 is None or img2 is None:
      print("Erro: Não foi possível carregar uma ou ambas as imagens. Verifique o caminho e nome dos arquivos.")
      exit()

   orb = cv2.ORB_create()

   kp1, des1 = orb.detectAndCompute(img1, None)
   kp2, des2 = orb.detectAndCompute(img2, None)

   if des1 is None or des2 is None:
      print("Não há descritores suficientes nas imagens para comparação.")
      exit()

   bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True) 

   matches = bf.match(des1, des2)
   matches = sorted(matches, key = lambda x:x.distance)

   MIN_MATCH_COUNT = min_match_count 

   if len(matches) > MIN_MATCH_COUNT:
      src_pts = np.float32([ kp1[m.queryIdx].pt for m in matches ]).reshape(-1,1,2)
      dst_pts = np.float32([ kp2[m.trainIdx].pt for m in matches ]).reshape(-1,1,2)

      M, mask = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC, 5.0)

      matchesMask = mask.ravel().tolist()
      inlier_count = sum(matchesMask)
      
      print(f"\n✅ Total de Pontos Validados (Inliers): {inlier_count}")

      if inlier_count >= MIN_MATCH_COUNT:
         print("➡️ DECISÃO: As imagens SÃO do mesmo lugar (alto número de inliers).")
      else:
         print("➡️ DECISÃO: As imagens NÃO são do mesmo lugar (baixo número de inliers).")


      draw_params = dict(matchColor = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)),
                        singlePointColor = None,
                        matchesMask = matchesMask, 
                        flags = 2)

      img_matches = cv2.drawMatches(img1, kp1, img2, kp2, matches, None, **draw_params)

      output_filename = "track_output.png" 
      cv2.imwrite(output_filename, img_matches)
      print(f"🖼️ Imagem do track salva como: {output_filename}")
      # cv2.imshow("Track de Pontos Validados", img_matches)
      # cv2.waitKey(0)
      # cv2.destroyAllWindows()

   else:
      print(f"\n❌ Não há matches suficientes ({len(matches)}). Mínimo exigido: {MIN_MATCH_COUNT}.")
      print("➡️ DECISÃO: As imagens NÃO são do mesmo lugar.")
   
   return

place_image_matcher('stonehenge2.png', 'stonehenge1.png', 10)